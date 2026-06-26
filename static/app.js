// Robot arm kinematics and state parameters
const L1 = 150; // Lower arm link length
const L2 = 130; // Upper arm link length
const BASE_X = 100; // Base joint X
const BASE_Y = 390; // Base joint Y (where it pivots)
const IDLE_X = 150;
const IDLE_Y = 220;

// Current state values
let currentArmX = IDLE_X;
let currentArmY = IDLE_Y;
let currentClawOpen = 12; // Claw finger angle (degrees)
let isAnimating = false;
let heldItemIndex = null;
let uploadedFile = null;

// Food items configuration (Demo data)
const foodItems = [
  {
    name: "Super-Juice Organic Berry",
    width: 30,
    height: 50,
    grabX: 245,
    grabY: 338,
    scanX: 105,
    scanY: 319,
    dx: -15,
    dy: 7,
    confidence: "99.4%",
    license: "10021021000123 (Verified)",
    safetyScore: 98,
    ingredients: ["Organic Apple Juice", "Cherry Pulp", "Vitamin C", "Natural Beet Color", "Stevia Leaf Extract"],
    checks: [
      { text: "FSSAI License: Valid & Verified", status: "success" },
      { text: "Allergen screening: Safe (0 allergens found)", status: "success" },
      { text: "Preservative check: 100% natural, no synthetic additives", status: "success" }
    ],
    highlightCard: "feature-fssai",
    statusText: "Active Scan",
    terminalLines: [
      "[SYS] CONNECTING TO FSSAI SECURITY NETWORK...",
      "[OCR] EXTRACTING LABEL: FRUIT JUICE 90%, CHERRY EXTRACT 10%",
      "[OCR] FSSAI LICENSE REGISTERED #10021021000123",
      "[SYS] LICENSE INTEGRITY VERIFIED. CRYPTO SIGNATURE OK.",
      "[SYS] STATUS: COMPLIANT. NO SYNTHETIC PRESERVATIVES FOUND."
    ]
  },
  {
    name: "NutriMax Keto Protein Bar",
    width: 40,
    height: 30,
    grabX: 320,
    grabY: 350,
    scanX: 105,
    scanY: 331,
    dx: -20,
    dy: 15,
    confidence: "97.8%",
    license: "11219034000854 (Verified)",
    safetyScore: 82,
    ingredients: ["Rolled Oats", "Whey Protein Isolate", "Almond Butter", "Glycerin", "Sucralose (E955)", "Soy Lecithin"],
    checks: [
      { text: "FSSAI License: Valid & Active", status: "success" },
      { text: "Allergen screening: Warning (Contains Almonds & Soy)", status: "warn" },
      { text: "Additive Warning: Contains Sucralose (artificial sweetener)", status: "warn" }
    ],
    highlightCard: "feature-risk",
    statusText: "Warning Found",
    terminalLines: [
      "[SYS] DETECTED INGREDIENTS LIST MATRIX...",
      "[OCR] EXTRACTING: WHEY PROTEIN, ALMONDS, SUCRALOSE",
      "[SYS] RUNNING RISK ASSESSMENT ON EU/FDA RESTRICTED ADDITIVES...",
      "[RISK] WARNING: E955 (SUCRALOSE) IDENTIFIED.",
      "[SYS] STATUS: PASS WITH DIETARY WARNINGS."
    ]
  },
  {
    name: "FizzUp Energy Soda - Neon Blue",
    width: 24,
    height: 45,
    grabX: 382,
    grabY: 343,
    scanX: 105,
    scanY: 321,
    dx: -14,
    dy: 7,
    confidence: "98.2%",
    license: "10014011001890 (Active)",
    safetyScore: 45,
    ingredients: ["Carbonated Water", "High Fructose Corn Syrup", "Phosphoric Acid (E338)", "Sodium Benzoate (E211)", "Caffeine", "Brilliant Blue FCF (E133)"],
    checks: [
      { text: "FSSAI License: Valid & Registered", status: "success" },
      { text: "Additive Warning: High Density of Preservatives (E211, E338)", status: "fail" },
      { text: "Synthetic Color: E133 (Brilliant Blue) requires warning label", status: "fail" }
    ],
    highlightCard: "feature-additive",
    statusText: "Flagged",
    terminalLines: [
      "[SYS] SCANNING COLOR SPECTRUM AND COMPONENT CODES...",
      "[OCR] EXTRACTING: HFCS, E338, E211, E133",
      "[SYS] CROSS-REFERENCING INGREDIENT SAFETY INDEX...",
      "[RISK] RED FLAG: E211 (SODIUM BENZOATE) EXCEEDS DAILY MARGIN.",
      "[SYS] STATUS: AUDIT FAILED. UNHEALTHY SYNTHETIC CONCENTRATION."
    ]
  },
  {
    name: "OatyFlakes Honey & Almond Cereal",
    width: 30,
    height: 60,
    grabX: 445,
    grabY: 335,
    scanX: 105,
    scanY: 316,
    dx: -15,
    dy: 0,
    confidence: "99.1%",
    license: "10018022000456 (Verified)",
    safetyScore: 75,
    ingredients: ["Whole Grain Wheat", "Oat Bran", "Almond Slices", "Honey", "Malt Extract", "Iron & Zinc Minerals"],
    checks: [
      { text: "FSSAI License: Valid & Authenticated", status: "success" },
      { text: "Allergen Warning: Contains Gluten (Wheat) & Almonds", status: "fail" },
      { text: "Chemical Additive: 0% Synthetic preservatives", status: "success" }
    ],
    highlightCard: "feature-ocr",
    statusText: "Allergens Found",
    terminalLines: [
      "[SYS] INGESTING HIGH RESOLUTION FRONT-OF-PACK LOGS...",
      "[OCR] EXTRACTING: WHOLE WHEAT, OAT BRAN, ALMONDS",
      "[SYS] MATCHING ALLERGEN PATTERNS...",
      "[OCR] DETECTED: WHEAT (GLUTEN), ALMOND (TREE NUT)",
      "[SYS] STATUS: COMPLIANT WITH MANDATORY ALLERGEN DISCLOSURE."
    ]
  }
];

// SVG Elements
const armLink1 = document.getElementById("arm-link-1");
const armLink1Detail = document.getElementById("arm-link-1-detail");
const armLink2 = document.getElementById("arm-link-2");
const armLink2Detail = document.getElementById("arm-link-2-detail");
const robotElbow = document.getElementById("robot-elbow");
const robotWrist = document.getElementById("robot-wrist");
const robotGripper = document.getElementById("robot-gripper");
const clawLeft = document.getElementById("claw-left");
const clawRight = document.getElementById("claw-right");
const itemCustom = document.getElementById("item-custom");

// Scanner Bed Elements
const scannerLaser = document.getElementById("scanner-laser");
const scannerLightBeam = document.getElementById("scanner-light-beam");
const scanningHud = document.getElementById("scanning-hud");
const hudProgressBarFill = document.getElementById("hud-progress-bar-fill");
const hudVerification = document.getElementById("hud-verification");
const hudText = document.getElementById("hud-text");
const robotStatusText = document.getElementById("robot-status-text");
const statusPulseIndicator = document.getElementById("status-pulse-indicator");

// Terminal & Report elements
const terminalPlaceholder = document.getElementById("terminal-placeholder");
const reportItemName = document.getElementById("report-item-name");
const reportItemConfidence = document.getElementById("report-item-confidence");
const reportItemLicense = document.getElementById("report-item-license");
const reportIngredientsList = document.getElementById("report-ingredients-list");
const reportComplianceChecks = document.getElementById("report-compliance-checks");
const scoreCircle = document.getElementById("score-circle");
const scoreValue = document.getElementById("score-value");
const safetyRatingText = document.getElementById("safety-rating-text");

// Update robotic arm joints on SVG
function updateArmJoints(targetX, targetY, clawOpenVal) {
  const dx = targetX - BASE_X;
  const dy = targetY - BASE_Y;
  let D = Math.sqrt(dx * dx + dy * dy);

  // Arm safety clamps
  const maxReach = L1 + L2 - 5;
  if (D > maxReach) {
    const angle = Math.atan2(dy, dx);
    targetX = BASE_X + maxReach * Math.cos(angle);
    targetY = BASE_Y + maxReach * Math.sin(angle);
    D = maxReach;
  }

  // Inverse Kinematics calculations
  const theta = Math.atan2(targetY - BASE_Y, targetX - BASE_X);
  const cosAlpha = (L1 * L1 + D * D - L2 * L2) / (2 * L1 * D);
  const alpha = Math.acos(Math.max(-1, Math.min(1, cosAlpha)));

  // Elbow coordinate (Elbow Up configuration)
  // Elbow coordinate (Elbow Down configuration)
  const elbowX = BASE_X + L1 * Math.cos(theta - alpha);
  const elbowY = BASE_Y + L1 * Math.sin(theta - alpha);

  // Update SVG DOM elements
  armLink1.setAttribute("x1", BASE_X);
  armLink1.setAttribute("y1", BASE_Y);
  armLink1.setAttribute("x2", elbowX);
  armLink1.setAttribute("y2", elbowY);

  armLink1Detail.setAttribute("x1", BASE_X);
  armLink1Detail.setAttribute("y1", BASE_Y - 10);
  armLink1Detail.setAttribute("x2", elbowX);
  armLink1Detail.setAttribute("y2", elbowY);

  robotElbow.setAttribute("transform", `translate(${elbowX}, ${elbowY})`);

  armLink2.setAttribute("x1", elbowX);
  armLink2.setAttribute("y1", elbowY);
  armLink2.setAttribute("x2", targetX);
  armLink2.setAttribute("y2", targetY);

  armLink2Detail.setAttribute("x1", elbowX);
  armLink2Detail.setAttribute("y1", elbowY);
  armLink2Detail.setAttribute("x2", targetX);
  armLink2Detail.setAttribute("y2", targetY);

  robotWrist.setAttribute("transform", `translate(${targetX}, ${targetY})`);
  robotGripper.setAttribute("transform", `translate(${targetX}, ${targetY})`);

  clawLeft.setAttribute("transform", `rotate(${clawOpenVal}, -8, 12)`);
  clawRight.setAttribute("transform", `rotate(${-clawOpenVal}, 8, 12)`);

  // Move held items
  if (heldItemIndex !== null) {
    if (heldItemIndex === "custom") {
      const itemTranslateX = targetX - 15;
      const itemTranslateY = targetY;
      itemCustom.setAttribute("transform", `translate(${itemTranslateX}, ${itemTranslateY})`);
    } else {
      const itemConfig = foodItems[heldItemIndex];
      const itemSvg = document.getElementById(`item-${heldItemIndex}`);
      const itemTranslateX = targetX + itemConfig.dx;
      const itemTranslateY = targetY + itemConfig.dy;
      itemSvg.setAttribute("transform", `translate(${itemTranslateX}, ${itemTranslateY})`);
    }
  }

  currentArmX = targetX;
  currentArmY = targetY;
  currentClawOpen = clawOpenVal;
}

function easeInOutQuad(t) {
  return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
}

function animateArmTo(targetX, targetY, targetClaw, duration, callback) {
  const startX = currentArmX;
  const startY = currentArmY;
  const startClaw = currentClawOpen;
  const startTime = performance.now();

  function step(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const ease = easeInOutQuad(progress);

    const x = startX + (targetX - startX) * ease;
    const y = startY + (targetY - startY) * ease;
    const claw = startClaw + (targetClaw - startClaw) * ease;

    updateArmJoints(x, y, claw);

    if (progress < 1) {
      requestAnimationFrame(step);
    } else {
      if (callback) callback();
    }
  }
  requestAnimationFrame(step);
}

// Custom file upload handlers
function triggerFileUploader() {
  document.getElementById("file-uploader").click();
}

function handleFileSelected(event) {
  const file = event.target.files[0];
  if (!file) return;
  
  uploadedFile = file;
  
  // Show Custom Item document on conveyor belt
  itemCustom.style.display = "block";
  itemCustom.setAttribute("transform", `translate(485, 335)`);
  
  // Trigger robot arm to pick custom label
  selectAndScanCustomItem();
}

// Stream terminal logs characters
function streamTerminalText(lines, callback) {
  terminalPlaceholder.style.display = "none";
  let currentLineIdx = 0;
  let currentCharIdx = 0;

  for (let i = 1; i <= 5; i++) {
    document.getElementById(`t-line-${i}`).innerHTML = "";
    document.getElementById(`t-line-${i}`).className = "terminal-line";
  }

  function typeChar() {
    if (currentLineIdx >= lines.length) {
      if (callback) callback();
      return;
    }

    const currentLineElement = document.getElementById(`t-line-${currentLineIdx + 1}`);
    const textToType = lines[currentLineIdx];

    if (textToType.startsWith("[SYS]")) {
      currentLineElement.classList.add("t-cyan");
    } else if (textToType.startsWith("[RISK]") || textToType.startsWith("[OCR] DETECTED:") || textToType.startsWith("[OCR] WARNING")) {
      currentLineElement.classList.add("t-warning");
    } else if (textToType.includes("FAILED") || textToType.includes("RED FLAG") || textToType.includes("ERROR")) {
      currentLineElement.classList.add("t-danger");
    } else if (textToType.includes("VERIFIED") || textToType.includes("COMPLIANT") || textToType.includes("SUCCESS")) {
      currentLineElement.classList.add("t-success");
    }

    currentLineElement.innerHTML += textToType.charAt(currentCharIdx);
    currentCharIdx++;

    if (currentCharIdx < textToType.length) {
      setTimeout(typeChar, 10);
    } else {
      currentLineIdx++;
      currentCharIdx = 0;
      setTimeout(typeChar, 80);
    }
  }

  typeChar();
}

// Render reports dynamically
function updateScanReport(reportData, customName = null) {
  let name = reportData.product_info ? (reportData.product_info.product_name || "Extracted Food Product") : "Custom Label Product";
  if (customName) name = customName;

  let confidence = reportData.confidence || "96.4%";
  let licenseText = "Not Detected";
  let licenseStatus = "fail";

  if (reportData.fssai) {
    if (typeof reportData.fssai === 'string') {
      licenseText = reportData.fssai;
    } else if (reportData.fssai.license_number) {
      licenseText = reportData.fssai.license_number;
      if (reportData.fssai.is_valid) {
        licenseText += " (Verified)";
        licenseStatus = "success";
      } else {
        licenseText += " (Invalid)";
      }
    }
  }

  reportItemName.textContent = name;
  reportItemName.classList.add("highlight-cyan");
  reportItemConfidence.textContent = confidence;
  reportItemLicense.textContent = licenseText;

  // Ingredients List
  reportIngredientsList.innerHTML = "";
  let ingredients = [];
  if (reportData.product_info && reportData.product_info.ingredients) {
    ingredients = reportData.product_info.ingredients;
  } else if (reportData.ingredients) {
    ingredients = reportData.ingredients;
  }

  if (ingredients.length === 0) {
    reportIngredientsList.innerHTML = `<span class="placeholder-text">No ingredients extracted.</span>`;
  } else {
    ingredients.forEach(ing => {
      const chip = document.createElement("span");
      chip.className = "ing-chip";
      chip.textContent = ing;
      
      const lowerIng = ing.toLowerCase();
      if (lowerIng.includes("sweetener") || lowerIng.includes("almond") || lowerIng.includes("soy") || lowerIng.includes("wheat") || lowerIng.includes("gluten")) {
        chip.classList.add("warning");
      } else if (lowerIng.match(/e\d+/) || lowerIng.includes("preservative") || lowerIng.includes("benzoate") || lowerIng.includes("acid")) {
        chip.classList.add("hazard");
      } else {
        chip.classList.add("safe");
      }
      reportIngredientsList.appendChild(chip);
    });
  }

  // Compliance checks list
  reportComplianceChecks.innerHTML = "";
  const checks = [];
  
  // FSSAI license check
  if (reportData.fssai && reportData.fssai.is_valid) {
    checks.push({ text: "FSSAI License: Valid & Verified", status: "success" });
  } else if (reportData.fssai && reportData.fssai.license_number) {
    checks.push({ text: "FSSAI License: Detected but invalid format", status: "warn" });
  } else {
    checks.push({ text: "FSSAI License: Missing on packaging label", status: "fail" });
  }

  // Allergen Check
  let allergens = reportData.product_info ? reportData.product_info.allergens : [];
  if (allergens && allergens.length > 0) {
    checks.push({ text: `Allergen Warning: Contains ${allergens.join(', ')}`, status: "warn" });
  } else {
    checks.push({ text: "Allergen screening: No common allergens declared", status: "success" });
  }

  // Additives Check
  let additives = reportData.additives || [];
  if (additives.length > 0) {
    const dangerous = additives.filter(a => a.risk_level === 'High Concern').length;
    if (dangerous > 0) {
      checks.push({ text: `Additives Check: Flagged ${additives.length} additives (${dangerous} dangerous)`, status: "fail" });
    } else {
      checks.push({ text: `Additives Check: Identified ${additives.length} safe/moderate additives`, status: "warn" });
    }
  } else {
    checks.push({ text: "Additives Check: 0 synthetic additives detected", status: "success" });
  }

  checks.forEach(chk => {
    const li = document.createElement("li");
    li.className = chk.status;
    const span = document.createElement("span");
    span.textContent = chk.status === "success" ? "✔" : chk.status === "warn" ? "⚠" : "✖";
    li.appendChild(span);
    li.appendChild(document.createTextNode(" " + chk.text));
    reportComplianceChecks.appendChild(li);
  });

  // Risk Score to Safety Index score circle conversion
  const riskScore = reportData.risk_score !== undefined ? reportData.risk_score : 50;
  const safetyScore = 100 - riskScore;

  let currentVal = 0;
  const scoreStartTime = performance.now();

  function animateScore(now) {
    const progress = Math.min((now - scoreStartTime) / 1000, 1);
    currentVal = Math.floor(safetyScore * progress);

    scoreCircle.style.strokeDasharray = `${currentVal}, 100`;
    scoreValue.textContent = `${currentVal}%`;

    if (currentVal > 85) {
      scoreCircle.style.stroke = "var(--green)";
      safetyRatingText.textContent = "Optimal Safety Rating. Food product fully complies with national regulatory requirements.";
    } else if (currentVal > 65) {
      scoreCircle.style.stroke = "var(--orange)";
      safetyRatingText.textContent = "Cautionary Rating. Presence of allergens or additives that require consumer disclosure.";
    } else {
      scoreCircle.style.stroke = "var(--red)";
      safetyRatingText.textContent = "High Risk. Presence of synthetic colorants or preservatives exceeding daily recommended limits.";
    }

    if (progress < 1) {
      requestAnimationFrame(animateScore);
    }
  }
  requestAnimationFrame(animateScore);

  // Core Features Dashboard Highlights
  document.querySelectorAll(".feature-card").forEach(card => {
    card.classList.remove("card-glow-active");
    card.querySelector(".feature-status-light").classList.remove("feature-status-active");
  });

  // Select core feature card based on highlights
  let cardId = "feature-ocr";
  let statusTxt = "Active";
  let levelColor = "var(--cyan)";

  if (riskScore > 60) {
    cardId = "feature-additive";
    statusTxt = "Flagged";
    levelColor = "var(--red)";
  } else if (riskScore > 40) {
    cardId = "feature-risk";
    statusTxt = "Warning Found";
    levelColor = "var(--orange)";
  } else if (licenseStatus === "success") {
    cardId = "feature-fssai";
    statusTxt = "Verified Secure";
    levelColor = "var(--green)";
  }

  const activeCard = document.getElementById(cardId);
  if (activeCard) {
    const glowCol = levelColor === "var(--red)" ? "rgba(239, 68, 68, 0.4)" : levelColor === "var(--orange)" ? "rgba(245, 158, 11, 0.4)" : "rgba(16, 185, 129, 0.4)";
    activeCard.style.setProperty("--glow-color", glowCol);
    activeCard.classList.add("card-glow-active");

    const statLight = activeCard.querySelector(".feature-status-light");
    statLight.classList.add("feature-status-active");
    statLight.textContent = statusTxt;
    statLight.style.setProperty("--glow-text-color", levelColor);
    statLight.style.setProperty("--glow-border-color", levelColor.replace(")", ", 0.25)"));
    statLight.style.setProperty("--glow-bg-color", levelColor.replace(")", ", 0.1)"));
  }
}

// Scanner progress bar triggers
function triggerScannerSweeper(callback) {
  scanningHud.style.display = "flex";
  hudText.textContent = "SCANNING PACKAGING...";
  hudText.style.color = "var(--cyan)";
  hudVerification.style.opacity = 0;
  hudProgressBarFill.style.width = "0%";

  scannerLaser.style.opacity = "1";
  scannerLaser.classList.add("laser-active");
  scannerLightBeam.style.opacity = "1";

  let progress = 0;
  const interval = setInterval(() => {
    progress += 4;
    hudProgressBarFill.style.width = `${progress}%`;
    if (progress >= 100) {
      clearInterval(interval);
      scannerLaser.classList.remove("laser-active");
      scannerLaser.style.opacity = "0";
      scannerLightBeam.style.opacity = "0";
      hudText.textContent = "SCAN COMPLETED";
      hudText.style.color = "var(--green)";
      if (callback) callback();
    }
  }, 100);
}

// Master state machine to select, move, pick, scan, place back, and return
function selectAndScanItem(itemIndex) {
  if (isAnimating) return;
  isAnimating = true;

  const item = foodItems[itemIndex];
  const itemSvg = document.getElementById(`item-${itemIndex}`);

  robotStatusText.textContent = "ARM IN MOTION";
  statusPulseIndicator.className = "status-pulse pulse-yellow";

  // Step 1: Open claws and move to target
  animateArmTo(item.grabX, item.grabY, 12, 1000, () => {
    robotStatusText.textContent = "GRABBING";
    // Step 2: Grab item (close claw)
    animateArmTo(item.grabX, item.grabY, 0, 400, () => {
      heldItemIndex = itemIndex;
      robotStatusText.textContent = "TRANSPORTING";

      // Step 3: Move carrying item to scanner
      animateArmTo(item.scanX, item.scanY, 0, 1200, () => {
        robotStatusText.textContent = "SCANNING OCR";
        statusPulseIndicator.className = "status-pulse pulse-green";

        // Step 4: Run sweepers
        triggerScannerSweeper(() => {
          updateScanReport(item);
          document.getElementById("report-section").scrollIntoView({ behavior: 'smooth' });
        });

        streamTerminalText(item.terminalLines, () => {
          robotStatusText.textContent = "RETURNING ITEM";
          statusPulseIndicator.className = "status-pulse pulse-yellow";

          setTimeout(() => {
            // Step 5: Place back
            animateArmTo(item.grabX, item.grabY, 0, 1200, () => {
              robotStatusText.textContent = "RELEASING";
              // Step 6: Open claws
              animateArmTo(item.grabX, item.grabY, 12, 400, () => {
                heldItemIndex = null;
                const origTranslateX = item.grabX + item.dx;
                const origTranslateY = item.grabY + item.dy;
                itemSvg.setAttribute("transform", `translate(${origTranslateX}, ${origTranslateY})`);

                // Step 7: Return idle
                robotStatusText.textContent = "RETURNING IDLE";
                animateArmTo(IDLE_X, IDLE_Y, 12, 800, () => {
                  robotStatusText.textContent = "SYSTEM READY";
                  statusPulseIndicator.className = "status-pulse pulse-green";
                  isAnimating = false;
                });
              });
            });
          }, 800);
        });
      });
    });
  });
}

// Pick and run custom uploaded image from python OCR backend
function selectAndScanCustomItem() {
  if (isAnimating) return;
  isAnimating = true;

  robotStatusText.textContent = "ARM IN MOTION";
  statusPulseIndicator.className = "status-pulse pulse-yellow";

  // Coordinates for the custom item (placed at x=485, y=335)
  const grabX = 495;
  const grabY = 335;
  const scanX = 105;
  const scanY = 316;

  // Step 1: Open claws and move to custom item
  animateArmTo(grabX, grabY, 12, 1000, () => {
    robotStatusText.textContent = "GRABBING";
    // Step 2: Grab the custom item (close claw)
    animateArmTo(grabX, grabY, 0, 400, () => {
      heldItemIndex = "custom";
      robotStatusText.textContent = "TRANSPORTING";

      // Step 3: Carry custom item to scanner bed
      animateArmTo(scanX, scanY, 0, 1200, () => {
        robotStatusText.textContent = "AI ANALYSIS ACTIVE";
        statusPulseIndicator.className = "status-pulse pulse-yellow";

        // Step 4: Run scanner sweeper HUD
        triggerScannerSweeper();

        // Concurrently stream terminal lines and trigger backend POST request
        const loadingTerminalLines = [
          "[SYS] DETECTED CUSTOM FOOD LABEL ENVELOPE...",
          "[SYS] LAUNCHING PYTHON OCR PIPELINE (EASYOCR)...",
          "[SYS] PARSING EXTRACTED TEXT VIA AI MATRIX...",
          "[SYS] EVALUATING FSSAI LICENSE & REGULATORY SCORES..."
        ];

        // Custom terminal loading stream loop
        streamTerminalText(loadingTerminalLines);

        // API Upload Request
        const formData = new FormData();
        formData.append('file', uploadedFile);

        console.log("[JS] Uploading label file to server...");
        fetch('/api/scan', {
          method: 'POST',
          body: formData
        })
        .then(response => {
          if (!response.ok) {
            throw new Error(`Server returned status ${response.status}`);
          }
          return response.json();
        })
        .then(data => {
          console.log("[JS] API scan response successfully received:", data);
          robotStatusText.textContent = "SCAN RESOLVED";
          statusPulseIndicator.className = "status-pulse pulse-green";

          // Stream real result lines on terminal
          const resultLines = [
            "[SYS] AI ANALYSIS FINISHED SUCCESSFULLY.",
            `[OCR] PRODUCT: ${data.product_info ? (data.product_info.product_name || "Unknown Product") : "Unknown"}`.substring(0, 45),
            `[OCR] INGREDIENTS DETECTED: ${data.product_info && data.product_info.ingredients ? data.product_info.ingredients.length : 0} items`,
            `[SYS] FSSAI STATUS: ${data.fssai ? data.fssai.status || "Not Checked" : "No License Found"}`,
            `[SYS] CALCULATED SAFETY INDEX: ${100 - (data.risk_score || 50)}%`
          ];

          streamTerminalText(resultLines, () => {
            // Update report view
            updateScanReport(data, uploadedFile.name);
            hudVerification.style.opacity = (data.fssai && data.fssai.is_valid) ? 1 : 0;
            
            // Scroll to report view
            document.getElementById("report-section").scrollIntoView({ behavior: 'smooth' });

            // Put item back and complete cycle
            setTimeout(() => {
              robotStatusText.textContent = "RETURNING CUSTOM";
              statusPulseIndicator.className = "status-pulse pulse-yellow";

              animateArmTo(grabX, grabY, 0, 1200, () => {
                robotStatusText.textContent = "RELEASING";
                animateArmTo(grabX, grabY, 12, 400, () => {
                  heldItemIndex = null;
                  itemCustom.setAttribute("transform", `translate(485, 335)`);
                  itemCustom.style.display = "none"; // Hide custom document shape

                  // Return to idle standby
                  robotStatusText.textContent = "RETURNING IDLE";
                  animateArmTo(IDLE_X, IDLE_Y, 12, 800, () => {
                    robotStatusText.textContent = "SYSTEM READY";
                    statusPulseIndicator.className = "status-pulse pulse-green";
                    isAnimating = false;
                    uploadedFile = null;
                  });
                });
              });
            }, 1000);
          });
        })
        .catch(err => {
          console.error("[JS ERROR] Error uploading file:", err);
          robotStatusText.textContent = "SCAN ERROR";
          statusPulseIndicator.className = "status-pulse pulse-red";

          const errorLines = [
            "[SYS] PIPELINE ERROR ENCOUNTERED.",
            `[ERROR] DETAILS: ${err.message}`,
            "[SYS] RETRY UPLOAD WITH CLEAN IMAGE RESOLUTION.",
            "[SYS] STANDBY FOR RESET PROTOCOL...",
            "[SYS] SYSTEM RETRACTED."
          ];

          streamTerminalText(errorLines, () => {
            // Put item back on error
            setTimeout(() => {
              animateArmTo(grabX, grabY, 12, 1000, () => {
                heldItemIndex = null;
                itemCustom.style.display = "none";
                animateArmTo(IDLE_X, IDLE_Y, 12, 800, () => {
                  robotStatusText.textContent = "SYSTEM READY";
                  statusPulseIndicator.className = "status-pulse pulse-green";
                  isAnimating = false;
                  uploadedFile = null;
                });
              });
            }, 1500);
          });
        });
      });
    });
  });
}

// Feature Card Mouse Tracking Shine Effect
document.querySelectorAll('.feature-card').forEach(card => {
  card.addEventListener('mousemove', e => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    card.style.setProperty('--mouse-x', `${x}px`);
    card.style.setProperty('--mouse-y', `${y}px`);
  });
});

// Initialize robotic arm on window loads
window.addEventListener("load", () => {
  updateArmJoints(IDLE_X, IDLE_Y, 12);
  
  // Dynamic stats counting effect on load
  const labelsCount = document.getElementById("stat-labels");
  const accuracyCount = document.getElementById("stat-accuracy");
  const countriesCount = document.getElementById("stat-countries");
  
  animateValue(labelsCount, 0, 500, 2000, "+");
  animateValueDecimal(accuracyCount, 0.0, 99.9, 2000, "%");
  animateValue(countriesCount, 0, 200, 2000, "+");
});

// Helper for dynamic counting
function animateValue(obj, start, end, duration, suffix = "") {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    obj.innerHTML = Math.floor(progress * (end - start) + start) + suffix;
    if (progress < 1) {
      window.requestAnimationFrame(step);
    }
  };
  window.requestAnimationFrame(step);
}

function animateValueDecimal(obj, start, end, duration, suffix = "") {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    const value = (progress * (end - start) + start).toFixed(1);
    obj.innerHTML = value + suffix;
    if (progress < 1) {
      window.requestAnimationFrame(step);
    }
  };
  window.requestAnimationFrame(step);
}
