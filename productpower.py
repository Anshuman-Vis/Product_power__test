"""
ProductPower FSSAI - Main Class (Optimized & Fixed)
"""
import joblib, easyocr, os, re, json, tempfile
from transformers import pipeline
from additives_database import find_additives_in_text
from fssai_validator import extract_fssai_number, validate_fssai
from risk_scorer import calculate_food_risk_score, get_risk_category

class llm_nutritionist():
    def __init__(self, lang_list=['en']):
        print("🔄 Initializing Models & OCR...")
        self.reader = easyocr.Reader(lang_list)
        self.pipe = pipeline("text-generation", model="google/flan-t5-small")
        self.prompt = 'Extract food product information and return as JSON:\n{"product_name":"","brand_name":"","ingredients":[],"nutrition":{"energy":"","protein":"","carbohydrate":"","sugar":"","fat":"","saturated_fat":"","sodium":""},"serving_size":"","net_weight":"","allergens":[]}\nText: '
        
        try:
            self.ml_model = joblib.load("models/food_risk_model.pkl")
            self.label_enc = joblib.load("models/risk_label_encoder.pkl")
        except:
            self.ml_model, self.label_enc = None, None

        self.data_text, self.data_json, self.data_nutritionist, self.additives, self.fssai_info, self.risk_score, self.risk_breakdown = None, {}, None, [], None, 0, {}

    def read_text(self, img_path):
        if img_path.lower().endswith('.pdf'):
            try:
                from pdf2image import convert_from_path
                txt = []
                for page in convert_from_path(img_path):
                    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                        page.save(tmp.name, 'JPEG')
                        txt.append('\n'.join([r[1] for r in self.reader.readtext(tmp.name)]))
                        os.unlink(tmp.name)
                return '\n'.join(txt)
            except Exception as e: return ""
        return '\n'.join([r[1] for r in self.reader.readtext(img_path)])

    def _parse_and_merge_data(self, text, llm_out):
        """Extracts JSON and uses regex fallback to fill missing LLM data (Fixes the zero-risk bug)"""
        data = {"product_name": "", "brand_name": "", "ingredients": [], "nutrition": {}}
        try:
            m = re.search(r"\{.*\}", str(llm_out), re.DOTALL)
            if m: data.update(json.loads(m.group(0)))
        except: pass

        # Fallback ignoring "100g" table headers
        c_txt = re.sub(r'100\s*[gm]l?\b', '', text, flags=re.IGNORECASE)
        get_n = lambda p: (re.search(p + r'[^\d]*(\d+(?:\.\d+)?)', c_txt, re.IGNORECASE) or [None, ""])[1]
        
        fb_nut = {k: get_n(p) for k, p in [('energy','energy'), ('protein','protein'), ('carbohydrate',r'carbo\w*'), ('sugar',r'sugar[s]?'), ('fat',r'(?:total\s+)?fat'), ('saturated_fat','saturated'), ('sodium','sodium')]}
        
        data['nutrition'] = data.get('nutrition') if isinstance(data.get('nutrition'), dict) else {}
        for k, v in fb_nut.items():
            if not data['nutrition'].get(k) or str(data['nutrition'][k]).strip() == "":
                data['nutrition'][k] = v

        if not data.get('ingredients'):
            ing_m = re.search(r'ingredients?[:\s]*([^.]+)', text, re.IGNORECASE)
            data['ingredients'] = [i.strip() for i in ing_m.group(1).split(',')] if ing_m else []
        return data

    def _get_ml_features(self):
        sf = lambda v: float(re.sub(r'[^\d.]', '', str(v)) or 0)
        nut = self.data_json.get("nutrition", {})
        pres = sum(1 for a in self.additives if "preservative" in str(a.get("category", "")).lower())
        return [[sf(nut.get("sugar")), sf(nut.get("sodium")), sf(nut.get("saturated_fat")), len(self.additives), pres]]

    def analyze(self, img_path):
        self.data_text = self.read_text(img_path)
        
        # LLM + Fallback merge
        llm_out = self.pipe(self.prompt + self.data_text[:500], max_new_tokens=300)[0]["generated_text"] if self.data_text else ""
        self.data_json = self._parse_and_merge_data(self.data_text, llm_out)
        
        self.additives = find_additives_in_text(self.data_text)
        self.fssai_info = validate_fssai(extract_fssai_number(self.data_text))

        # Risk Scoring
        if self.ml_model and self.label_enc:
            fts = self._get_ml_features()
            cat = self.label_enc.inverse_transform([self.ml_model.predict(fts)[0]])[0]
            self.risk_score = {"Low": 20, "Moderate": 50, "High": 75, "Very High": 90}.get(cat, 50)
            self.risk_breakdown = {"ml_prediction": cat, "features": {"sugar": fts[0][0], "sodium": fts[0][1], "saturated_fat": fts[0][2], "additives_count": fts[0][3], "preservatives": fts[0][4]}}
        else:
            self.risk_score, self.risk_breakdown = calculate_food_risk_score(self.data_json, self.additives)

        if self.data_json.get('ingredients'):
            self.data_nutritionist = self.pipe("Explain these ingredients briefly: " + ', '.join(self.data_json['ingredients'][:10]), max_new_tokens=200)[0]["generated_text"]

        return self.get_full_report()

    def get_full_report(self):
        cat = self.risk_breakdown.get("ml_prediction", get_risk_category(self.risk_score)[0]) if self.ml_model else get_risk_category(self.risk_score)[0]
        return {"product_info": self.data_json, "additives": self.additives, "fssai": self.fssai_info, "risk_score": self.risk_score, "risk_category": cat, "risk_breakdown": self.risk_breakdown, "ingredient_analysis": self.data_nutritionist, "raw_text": self.data_text}

    def save(self, out="results"):
        os.makedirs(out, exist_ok=True)
        with open(f"{out}/report.json", "w", encoding='utf-8') as f: json.dump(self.get_full_report(), f, indent=2, default=str)
        if self.data_text:
            with open(f"{out}/text.txt", "w", encoding='utf-8') as f: f.write(self.data_text)