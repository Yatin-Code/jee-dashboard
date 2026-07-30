import json, re
from collections import defaultdict

BASE = "/data/data/com.termux/files/home/jee-analysis"

# ====== CHAPTER KEYWORD DATABASE ======
CHAPTER_KEYWORDS = {
    "physics": {
        "Kinematics": ["average speed", "average velocity", "projectile", "relative velocity", "free fall", "displacement of", "equations of motion", "uniform acceleration", "instantaneous velocity", "motion in a straight line", "velocity of", "acceleration of"],
        "Laws of Motion": ["newton's", "coefficient of friction", "free body diagram", "pulley", "tension in the string", "normal reaction", "inertia of", "contact force", "equilibrium of forces", "pseudo force", "friction between"],
        "Work Energy Power": ["work-energy theorem", "conservation of energy", "elastic potential", "potential energy", "work done by", "power of", "spring constant", "kinetic energy of"],
        "Rotational Motion": ["moment of inertia", "angular momentum", "angular velocity", "torque", "radius of gyration", "rotational kinetic energy", "rigid body", "angular acceleration", "rolling without slipping", "conservation of angular momentum"],
        "Gravitation": ["acceleration due to gravity", "escape velocity", "orbital velocity", "gravitational potential", "kepler's", "geostationary", "gravitational force", "satellite"],
        "Properties of Solids & Liquids": ["young's modulus", "bulk modulus", "shear modulus", "surface tension", "capillary", "bernoulli's", "viscosity", "terminal velocity", "stokes law", "buoyant", "strain"],
        "Thermodynamics": ["first law of thermodynamics", "carnot engine", "heat engine", "isothermal", "adiabatic", "internal energy of", "specific heat", "latent heat", "entropy of"],
        "Kinetic Theory of Gases": ["rms velocity", "mean free path", "kinetic theory of gases", "degree of freedom", "gas laws"],
        "Oscillations & Waves": ["simple harmonic motion", "shm", "time period of", "simple pendulum", "spring mass", "standing wave", "beats", "doppler effect", "speed of wave", "transverse wave", "longitudinal wave", "resonance in"],
        "Electrostatics": ["coulomb's law", "electric field", "electric potential", "gauss law", "capacitor", "dielectric", "electric dipole", "charge density", "electric flux", "capacitance of"],
        "Current Electricity": ["ohm's law", "kirchhoff's", "resistivity", "wheatstone bridge", "meter bridge", "potentiometer", "equivalent resistance", "internal resistance", "emf of", "conductivity of"],
        "Magnetic Effects & Magnetism": ["magnetic field", "biot-savart", "ampere circuital", "lorentz force", "cyclotron", "magnetic moment", "magnetic force", "earth's magnetic", "paramagnetic", "diamagnetic", "ferromagnetic"],
        "EMI & Alternating Current": ["faraday's law", "lenz law", "induced emf", "self inductance", "mutual inductance", "ac generator", "transformer", "impedance", "lcr circuit", "power factor", "eddy current"],
        "Optics": ["snell's law", "critical angle", "total internal reflection", "focal length", "lens maker", "magnification of", "young's double slit", "diffraction", "polarization", "refractive index", "mirror formula", "ray optics", "wave optics"],
        "Modern Physics": ["photoelectric effect", "stopping potential", "threshold frequency", "work function", "de broglie wavelength", "bohr model", "energy level of hydrogen", "nuclear fission", "nuclear fusion", "radioactive decay", "half life of", "binding energy of", "x-ray", "compton", "black body radiation"],
        "Electronic Devices": ["logic gate", "pn junction", "zener diode", "transistor", "rectifier", "semiconductor", "led", "solar cell", "and gate", "or gate", "not gate", "nand gate", "nor gate"],
        "EM Waves": ["electromagnetic wave", "em wave", "microwave", "infrared", "ultraviolet", "radio wave", "gamma ray", "electromagnetic spectrum"],
    },
    "chemistry": {
        "Basic Concepts": ["mole concept", "molarity of", "molality of", "normality of", "empirical formula", "molecular formula", "limiting reagent", "number of moles", "mass percentage"],
        "Atomic Structure": ["bohr model", "quantum number", "aufbau", "hund's", "pauli exclusion", "heisenberg uncertainty", "schrodinger", "azimuthal quantum", "spin quantum", "orbital"],
        "Chemical Bonding": ["ionic bond", "covalent bond", "vsepr", "hybridization of", "molecular orbital", "bond order", "dipole moment", "lattice energy", "formal charge", "hydrogen bond", "sigma bond", "pi bond", "resonance structure"],
        "Thermodynamics": ["enthalpy of", "entropy change", "gibbs free energy", "spontaneous reaction", "hess law", "born haber", "heat of combustion", "lattice energy of", "heat of formation"],
        "Equilibrium": ["equilibrium constant", "le chatelier", "dissociation constant", "buffer solution", "ph of", "poh", "solubility product", "common ion effect", "degree of dissociation"],
        "Redox & Electrochemistry": ["oxidation number", "redox reaction", "galvanic cell", "electrolytic cell", "nernst equation", "faraday's law", "conductivity of solution", "cell potential", "standard electrode"],
        "Chemical Kinetics": ["rate constant", "order of reaction", "activation energy", "arrhenius", "half life period", "first order reaction", "rate law", "molecularity of"],
        "Periodic Table": ["ionization enthalpy", "electron gain enthalpy", "electronegativity of", "atomic radius of", "s block", "p block", "d block", "lanthanoid contraction"],
        "Coordination Compounds": ["coordination number", "ligand", "crystal field splitting", "chelate", "spectrochemical series", "werner theory", "coordination compound"],
        "Hydrocarbons": ["alkane", "alkene", "alkyne", "benzene", "aromatic compound", "markovnikov", "ozonolysis", "hydrogenation of", "hydrocarbon"],
        "GOC": ["iupac name", "inductive effect", "resonance effect", "hyperconjugation", "mesomeric", "electrophile", "nucleophile", "carbocation", "carbanion", "functional group"],
        "Oxygen Compounds": ["alcohol", "phenol", "ether", "aldehyde", "ketone", "carboxylic acid", "ester", "cannizzaro", "aldol condensation", "oxidation of alcohol", "esterification"],
        "Nitrogen Compounds": ["amine", "amide", "nitro compound", "diazonium", "carbylamine", "hofmann degradation", "nitrogen compound"],
        "Biomolecules": ["glucose", "fructose", "sucrose", "amino acid", "protein", "enzyme", "vitamin", "dna", "rna", "nucleic acid", "carbohydrate", "peptide bond"],
        "Polymers": ["polymerization", "addition polymer", "condensation polymer", "monomer", "buna", "teflon", "nylon", "polyester", "polystyrene", "rubber"],
        "p-Block Elements": ["boron", "aluminium", "carbon family", "nitrogen family", "oxygen family", "halogen", "noble gas", "interhalogen", "sulphuric acid", "nitric acid", "ammonia"],
        "d & f Block": ["transition element", "lanthanide", "actinide", "oxidation state of", "colored ion", "magnetic moment of", "complex formation tendency", "d block element"],
        "Solid State": ["crystal lattice", "unit cell", "bragg", "packing efficiency", "schottky defect", "frenkel defect", "band theory", "semiconductor"],
        "Solutions": ["henry law", "raoult law", "colligative", "freezing point depression", "boiling point elevation", "osmotic pressure", "van hoff factor", "azeotrope"],
    },
    "mathematics": {
        "Sets Relations Functions": ["relation", "injective function", "surjective function", "bijective function", "one-one", "onto function", "composite function", "inverse of function", "domain of function", "range of function", "equivalence relation", "power set"],
        "Complex Numbers": ["complex number", "imaginary part", "modulus of", "argument of", "conjugate of", "de moivre", "cube root of unity", "argand", "complex plane"],
        "Sequences & Series": ["arithmetic progression", "geometric progression", "common difference", "common ratio", "harmonic progression", "sum of series", "infinite series", "a.p.", "g.p."],
        "Permutations & Combinations": ["permutation", "combination", "number of ways", "arrangement of", "selection of", "factorial", "ncr", "npr", "circular permutation"],
        "Binomial Theorem": ["binomial expansion", "binomial theorem", "general term of", "coefficient of x", "middle term in", "pascal triangle"],
        "Matrices & Determinants": ["matrix", "determinant of", "adjoint of", "inverse of matrix", "eigen value", "cramer rule", "system of equations", "singular matrix", "non singular"],
        "Coordinate Geometry": ["equation of line", "equation of circle", "parabola", "ellipse", "hyperbola", "focus of", "directrix of", "eccentricity", "tangent to", "normal to", "locus of", "slope of line", "centre of circle", "coordinate geometry"],
        "Limits Continuity Differentiability": ["limit of", "continuous function", "derivative of", "differentiability", "l hospital", "differentiation of"],
        "Integral Calculus": ["indefinite integral", "definite integral", "integration of", "area bounded by", "area under curve", "integration by parts", "substitution method", "partial fraction"],
        "Differential Equations": ["differential equation", "order of differential equation", "homogeneous equation", "exact differential", "integrating factor", "general solution of", "particular solution of"],
        "3D Geometry": ["direction cosine", "direction ratio", "equation of plane", "line in space", "shortest distance", "angle between lines", "angle between planes", "three dimensional geometry"],
        "Vector Algebra": ["dot product", "cross product", "scalar triple product", "vector triple product", "unit vector along", "position vector of", "projection of vector", "vector algebra"],
        "Probability": ["probability of", "bayes theorem", "conditional probability", "random variable", "expected value", "binomial distribution", "mutually exclusive", "independent event"],
        "Statistics": ["mean of", "median of", "mode of", "standard deviation", "variance of data", "correlation coefficient", "regression line"],
        "Trigonometry": ["sine of", "cosine of", "tangent of", "inverse trigonometric", "solution of triangle", "angle of elevation", "trigonometric equation"],
        "Quadratic Equations": ["quadratic equation", "nature of roots", "sum of roots", "product of roots", "discriminant of", "roots of equation"],
    }
}

def classify_question(text, subject):
    text_lower = text.lower()
    scores = defaultdict(float)
    
    for chapter, keywords in CHAPTER_KEYWORDS.get(subject, {}).items():
        for kw in keywords:
            if kw.lower() in text_lower:
                # Weight by specificity: longer = more specific
                weight = 1.0 + len(kw.split()) * 0.5
                scores[chapter] += weight
    
    if not scores:
        return "Unclassified"
    
    return max(scores, key=scores.get)

def extract_questions(text, subject):
    """Extract numbered questions from OCR text"""
    # Split on numbered patterns like "1." or "1)" or "Q.1"
    patterns = [
        r'\b(\d+)\.\s*(?=[A-Z])',    # "1. Two long..."
        r'\b(\d+)\)\s*(?=[A-Z])',     # "1) Two long..."
        r'\bQ\.(\d+)\s*',             # "Q.1 Two long..."
        r'\bQuestion\s*(\d+)\s*',     # "Question 1"
    ]
    
    questions = []
    
    # Try each pattern
    for pattern in patterns:
        splits = re.split(pattern, text)
        if len(splits) > 3:  # Found question numbering
            # Reconstruct: [prefix, num1, text1, num2, text2, ...]
            questions = []
            i = 1
            while i < len(splits) - 1:
                q_num = splits[i].strip()
                q_text = splits[i + 1].strip()
                # Check if this looks like a real question (has content)
                if len(q_text) > 20 and not q_text.startswith("SECTION"):
                    questions.append((q_num, q_text))
                i += 2
            if questions:
                break
    
    return questions

def extract_subject_sections(text):
    """Split combined paper text into Physics/Chemistry/Math sections"""
    sections = {"physics": "", "chemistry": "", "mathematics": ""}
    
    # Look for section headers
    # Pattern: "SECTION-A" or "PHYSICS" or similar headers
    phys_patterns = [r'PHYSICS', r'SECTION-A', r'SECTION A']
    chem_patterns = [r'CHEMISTRY', r'SECTION-B', r'SECTION B']
    math_patterns = [r'MATHEMATICS', r'SECTION-C', r'SECTION C']
    
    # Find positions
    phys_pos = float('inf')
    chem_pos = float('inf')
    math_pos = float('inf')
    
    for p in phys_patterns:
        idx = text.upper().find(p)
        if idx != -1 and idx < phys_pos:
            phys_pos = idx
    
    for p in chem_patterns:
        idx = text.upper().find(p)
        if idx != -1 and idx < chem_pos and idx > phys_pos:
            chem_pos = idx
    
    for p in math_patterns:
        idx = text.upper().find(p)
        if idx != -1 and idx < math_pos and idx > chem_pos:
            math_pos = idx
    
    if phys_pos != float('inf') and chem_pos != float('inf'):
        sections["physics"] = text[phys_pos:chem_pos]
    if chem_pos != float('inf') and math_pos != float('inf'):
        sections["chemistry"] = text[chem_pos:math_pos]
    if math_pos != float('inf'):
        sections["mathematics"] = text[math_pos:]
    
    return sections

# ====== MAIN PROCESSING ======
with open(f"{BASE}/raw_data/ocr_results.json") as f:
    ocr_data = json.load(f)

# Determine subject from paper ID
def get_subject(paper_id, url=""):
    """Determine subject from paper ID or URL"""
    pid = paper_id.lower()
    url_lower = url.lower()
    
    # Check URL first (more reliable for eSaral papers)
    for subj, keywords in [("mathematics", ["math"]), ("physics", ["physics"]), ("chemistry", ["chemistry", "chem"])]:
        for kw in keywords:
            if kw in url_lower:
                return subj
    
    # Fall back to ID
    for subj, keywords in [("mathematics", ["math"]), ("physics", ["physics", "phy"]), ("chemistry", ["chemistry", "chem"])]:
        for kw in keywords:
            if kw in pid:
                return subj
    return None

# Process all papers
results = {
    "mains": {"physics": defaultdict(int), "chemistry": defaultdict(int), "mathematics": defaultdict(int)},
    "advanced": {"physics": defaultdict(int), "chemistry": defaultdict(int), "mathematics": defaultdict(int)}
}

year_subject_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

for key, paper in ocr_data["papers"].items():
    text = paper["text"]
    pid = paper["id"]
    url = paper["url"]
    
    # Determine exam type and year
    if pid.startswith("adv"):
        exam_type = "advanced"
        year_str = pid.split("_")[1]
    elif pid.startswith("mains"):
        exam_type = "mains"
        year_str = pid.split("_")[1] if len(pid.split("_")) > 1 else "unknown"
    else:
        continue
    
    # Determine subject
    subject = get_subject(pid, url)
    
    # Combined papers (no subject in URL, and from 2025+ Mains or 2024+ Advanced)
    is_combined = subject is None
    
    if is_combined:
        # Combined paper - split by subject
        sections = extract_subject_sections(text)
        has_content = any(s.strip() for s in sections.values())
        if has_content:
            for subj, section_text in sections.items():
                if section_text.strip():
                    questions = extract_questions(section_text, subj)
                    for q_num, q_text in questions:
                        chapter = classify_question(q_text, subj)
                        results[exam_type][subj][chapter] += 1
                        year_subject_counts[year_str][subj][chapter] += 1
        else:
            # Couldn't find headers - try to identify subject from content keywords
            phys_kw = ["mass", "force", "velocity", "current", "circuit", "charge", "field", "lens", "mirror", "spring", "pendulum", "capacitor", "resistor", "magnetic", "wave", "photon"]
            chem_kw = ["mole", "reaction", "bond", "compound", "element", "acid", "base", "salt", "solution", "gas", "organic"]
            math_kw = ["equation", "function", "integral", "differentiate", "matrix", "vector", "probability", "angle", "triangle", "circle"]
            
            text_lower = text.lower()
            phys_score = sum(text_lower.count(kw) for kw in phys_kw)
            chem_score = sum(text_lower.count(kw) for kw in chem_kw)
            math_score = sum(text_lower.count(kw) for kw in math_kw)
            
            detected_subjects = {
                "physics": phys_score,
                "chemistry": chem_score,
                "mathematics": math_score
            }
            
            # Assign to best-matching subject
            best_subj = max(detected_subjects, key=detected_subjects.get)
            if max(phys_score, chem_score, math_score) > 5:
                questions = extract_questions(text, best_subj)
                for q_num, q_text in questions:
                    chapter = classify_question(q_text, best_subj)
                    results[exam_type][best_subj][chapter] += 1
                    year_subject_counts[year_str][best_subj][chapter] += 1
    else:
        # Subject-specific paper
        questions = extract_questions(text, subject)
        for q_num, q_text in questions:
            chapter = classify_question(q_text, subject)
            results[exam_type][subject][chapter] += 1
            year_subject_counts[year_str][subject][chapter] += 1

print("=== PARSING RESULTS ===")
for exam_type in ["mains", "advanced"]:
    print(f"\n--- {exam_type.upper()} ---")
    for subj in ["physics", "chemistry", "mathematics"]:
        chapters = results[exam_type][subj]
        if chapters:
            total = sum(chapters.values())
            print(f"\n  {subj.title()} ({total} questions classified):")
            for chapter, count in sorted(chapters.items(), key=lambda x: -x[1])[:15]:
                pct = count / total * 100
                print(f"    {chapter:35s} {count:4d} ({pct:5.1f}%)")

# Save results
output = {
    "total_papers": len(ocr_data["papers"]),
    "total_chars": ocr_data["metadata"]["total_chars"],
    "totals": {e: {s: dict(c) for s, c in subs.items() if c}
               for e, subs in results.items()},
    "yearly": {y: {s: dict(c) for s, c in subs.items() if c}
               for y, subs in year_subject_counts.items()}
}

with open(f"{BASE}/raw_data/parsed_questions.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\n\nSaved to raw_data/parsed_questions.json")
