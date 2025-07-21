import streamlit as st
import random

# Dictionary of questions for each experiment
quiz_questions = {
    "batch_reactor": [
        {
            "question": "What is the main advantage of a batch reactor?",
            "options": [
                "High throughput",
                "Flexibility for different products",
                "Low maintenance costs",
                "Continuous operation"
            ],
            "correct": 1,
            "explanation": "Batch reactors offer flexibility to produce different products in the same vessel, making them ideal for multiple product lines or test batches."
        },
        {
            "question": "Which of the following equations is used to model a first-order reaction in a batch reactor?",
            "options": [
                "-dC/dt = kC",
                "-dC/dt = kC²",
                "-dC/dt = k",
                "-dC/dt = k√C"
            ],
            "correct": 0,
            "explanation": "For a first-order reaction, the rate is proportional to the concentration, giving -dC/dt = kC."
        },
        {
            "question": "What parameter is typically plotted on the y-axis of a batch reactor design equation?",
            "options": [
                "Time",
                "1/(1-X) where X is conversion",
                "Concentration",
                "Temperature"
            ],
            "correct": 1,
            "explanation": "When designing a batch reactor, 1/(1-X) is often plotted against time to determine reaction kinetics."
        },
        {
            "question": "In a batch reactor, which of the following is constant?",
            "options": [
                "Composition",
                "Volume (for liquid phase reactions)",
                "Conversion",
                "Temperature (for non-isothermal reactions)"
            ],
            "correct": 1,
            "explanation": "In liquid-phase batch reactors, the volume typically remains constant while composition changes as the reaction proceeds."
        },
        {
            "question": "What happens to reactant concentration over time in a batch reactor?",
            "options": [
                "Remains constant",
                "Increases exponentially",
                "Decreases",
                "Oscillates"
            ],
            "correct": 2,
            "explanation": "Reactant concentration decreases over time as reactants are converted to products."
        },
        {
            "question": "Which parameter is most important in determining batch reactor size?",
            "options": [
                "Maximum allowable pressure",
                "Maximum reaction time",
                "Minimum conversion required",
                "All of the above"
            ],
            "correct": 3,
            "explanation": "Reactor size depends on all these factors: pressure limitations, required reaction time, and conversion targets."
        },
        {
            "question": "How does increasing temperature typically affect reaction rate in a batch reactor?",
            "options": [
                "Decreases reaction rate",
                "Increases reaction rate",
                "Has no effect on reaction rate",
                "First increases then decreases reaction rate"
            ],
            "correct": 1,
            "explanation": "According to the Arrhenius equation, increasing temperature generally increases the reaction rate constant."
        },
        {
            "question": "What is the space time for a batch reactor?",
            "options": [
                "Volume/Volumetric flow rate",
                "Time required to process one batch",
                "Residence time",
                "Batch reactors don't have a space time"
            ],
            "correct": 1,
            "explanation": "Space time for a batch reactor is the total time required to complete one batch, including filling, reaction, emptying, and cleaning."
        },
        {
            "question": "Which method is commonly used to determine reaction order in a batch reactor?",
            "options": [
                "Integral method",
                "Differential method",
                "Both A and B",
                "Neither A nor B"
            ],
            "correct": 2,
            "explanation": "Both integral and differential methods can be used to determine reaction order from batch reactor data."
        },
        {
            "question": "For a zero-order reaction in a batch reactor, how does the concentration change with time?",
            "options": [
                "C = C₀e^(-kt)",
                "C = C₀/(1+kC₀t)",
                "C = C₀ - kt",
                "C = C₀/(kt)"
            ],
            "correct": 2,
            "explanation": "For zero-order reactions, concentration decreases linearly with time: C = C₀ - kt."
        }
    ],
    "semi_batch_reactor": [
        {
            "question": "What is the key feature that distinguishes a semi-batch reactor from a batch reactor?",
            "options": [
                "Temperature control",
                "Continuous addition or removal of material during reaction",
                "Pressure control",
                "Catalyst addition"
            ],
            "correct": 1,
            "explanation": "Semi-batch reactors involve continuous addition or removal of reactants or products during the reaction process."
        },
        {
            "question": "Which of the following is a common reason to operate a reactor in semi-batch mode?",
            "options": [
                "To increase production capacity",
                "To control highly exothermic reactions",
                "To reduce equipment costs",
                "To simplify reactor design"
            ],
            "correct": 1,
            "explanation": "Semi-batch operation allows controlled addition of a reactant, helping manage heat release in highly exothermic reactions."
        },
        {
            "question": "In a semi-batch reactor, what typically happens to the volume?",
            "options": [
                "Remains constant",
                "Increases",
                "Decreases",
                "Any of the above, depending on the process"
            ],
            "correct": 3,
            "explanation": "Volume can increase (with addition), decrease (with removal), or be managed to remain constant, depending on the specific process."
        },
        {
            "question": "What type of reactions benefit most from semi-batch operation?",
            "options": [
                "Very slow reactions",
                "Very fast reactions",
                "Reactions with undesired side products at high concentrations",
                "Endothermic reactions"
            ],
            "correct": 2,
            "explanation": "Semi-batch operation helps control reactant concentrations, reducing unwanted side reactions that occur at high concentrations."
        },
        {
            "question": "The material balance for a semi-batch reactor includes terms for:",
            "options": [
                "Input flow only",
                "Output flow only",
                "Both input and output flows",
                "Neither input nor output flows"
            ],
            "correct": 2,
            "explanation": "The material balance must account for both material entering and leaving the system, plus reaction terms."
        },
        {
            "question": "Which industries commonly use semi-batch reactors?",
            "options": [
                "Petroleum refining",
                "Pharmaceutical and specialty chemicals",
                "Cement production",
                "Metal refining"
            ],
            "correct": 1,
            "explanation": "Semi-batch reactors are widely used in pharmaceutical and specialty chemical production where product quality and reaction control are critical."
        },
        {
            "question": "What is the primary advantage of a semi-batch reactor over a CSTR for highly exothermic reactions?",
            "options": [
                "Higher conversion",
                "Better temperature control",
                "Lower capital cost",
                "Higher throughput"
            ],
            "correct": 1,
            "explanation": "By controlling the addition rate of reactants, semi-batch reactors provide better temperature control for highly exothermic reactions."
        },
        {
            "question": "Which mass balance equation correctly describes a semi-batch reactor with no outflow?",
            "options": [
                "dN/dt = r·V",
                "dN/dt = F_in - r·V",
                "dN/dt = F_in + r·V",
                "dN/dt = F_in - F_out + r·V"
            ],
            "correct": 2,
            "explanation": "For a semi-batch reactor with only input, the mass balance is: dN/dt = F_in + r·V, where r is the reaction rate (negative for reactants)."
        },
        {
            "question": "What feeding policy might be used to maintain a constant concentration of a reactant in a semi-batch reactor?",
            "options": [
                "Constant feed rate",
                "Increasing feed rate over time",
                "Decreasing feed rate over time",
                "Exponentially increasing feed rate"
            ],
            "correct": 2,
            "explanation": "To maintain constant concentration of a reactant being consumed, the feed rate typically needs to decrease over time as the volume increases."
        },
        {
            "question": "Why might a semi-batch reactor be preferred over a batch reactor for reactions involving volatile compounds?",
            "options": [
                "Better mixing",
                "Ability to operate at lower pressures",
                "Reduced vapor space and emissions",
                "Higher temperature operation"
            ],
            "correct": 2,
            "explanation": "Adding volatile compounds gradually reduces the vapor space concentration, potentially reducing emissions and safety concerns."
        }
    ],
    "cstr": [
        {
            "question": "What does CSTR stand for?",
            "options": [
                "Continuous Stirred Tank Reactor",
                "Catalytic Surface Treatment Reactor",
                "Complete Solids Transfer Reactor",
                "Chemical Substrate Treatment Reactor"
            ],
            "correct": 0,
            "explanation": "CSTR stands for Continuous Stirred Tank Reactor, a type of reactor where contents are continuously mixed for uniform composition."
        },
        {
            "question": "What is the key assumption for an ideal CSTR?",
            "options": [
                "Plug flow behavior",
                "Perfect mixing with uniform composition throughout",
                "Zero backmixing",
                "No heat transfer with surroundings"
            ],
            "correct": 1,
            "explanation": "An ideal CSTR assumes perfect mixing, resulting in uniform concentration and temperature throughout the reactor."
        },
        {
            "question": "For a CSTR at steady state, the outlet concentration of reactant is equal to:",
            "options": [
                "The inlet concentration",
                "Zero",
                "The concentration inside the reactor",
                "Half the inlet concentration"
            ],
            "correct": 2,
            "explanation": "Due to perfect mixing, the concentration inside the reactor equals the outlet concentration in a CSTR."
        },
        {
            "question": "What is the residence time distribution in an ideal CSTR?",
            "options": [
                "Dirac delta function",
                "Normal distribution",
                "Exponential decay",
                "Uniform distribution"
            ],
            "correct": 2,
            "explanation": "The residence time distribution in an ideal CSTR follows an exponential decay pattern."
        },
        {
            "question": "What happens to conversion in a single CSTR as the reaction order increases (for the same space time)?",
            "options": [
                "Increases",
                "Decreases",
                "Remains the same",
                "First increases then decreases"
            ],
            "correct": 1,
            "explanation": "For the same space time, conversion in a CSTR decreases as reaction order increases due to the concentration-dependent nature of higher-order reactions."
        },
        {
            "question": "What is the space time for a CSTR?",
            "options": [
                "The time it takes to process one reactor volume",
                "Average time molecules spend in the reactor",
                "Volume divided by volumetric flow rate",
                "Both B and C"
            ],
            "correct": 3,
            "explanation": "Space time (τ) is V/v₀, which equals the average residence time of molecules in the reactor."
        },
        {
            "question": "For a first-order reaction in a CSTR, what is the relationship between conversion (X) and space time (τ)?",
            "options": [
                "X = 1 - e^(-kτ)",
                "X = kτ",
                "X = kτ/(1+kτ)",
                "X = 1 - 1/(1+kτ)"
            ],
            "correct": 2,
            "explanation": "For a first-order reaction in a CSTR, the relationship is X = kτ/(1+kτ)."
        },
        {
            "question": "Which reactor type generally requires larger volume than a CSTR for the same conversion?",
            "options": [
                "Batch reactor",
                "Plug flow reactor",
                "Semi-batch reactor",
                "CSTRs always require the largest volume"
            ],
            "correct": 3,
            "explanation": "CSTRs generally require larger volumes than PFRs or batch reactors for the same conversion due to their mixing characteristics."
        },
        {
            "question": "What is the main advantage of a CSTR over a PFR?",
            "options": [
                "Higher conversion",
                "Better temperature control",
                "Lower capital cost",
                "Higher selectivity"
            ],
            "correct": 1,
            "explanation": "CSTRs provide better temperature control due to their mixing characteristics, making them suitable for highly exothermic reactions."
        },
        {
            "question": "How many CSTRs in series would be needed to approximate a PFR?",
            "options": [
                "2-3",
                "5-10",
                "Infinite number",
                "Just one large CSTR"
            ],
            "correct": 2,
            "explanation": "An infinite number of CSTRs in series would perfectly approximate a PFR, though practically 10-20 can come close."
        }
    ],
    "pfr": [
        {
            "question": "What does PFR stand for?",
            "options": [
                "Pressurized Flow Reactor",
                "Plug Flow Reactor",
                "Partial Fill Reactor",
                "Packed Fuel Reactor"
            ],
            "correct": 1,
            "explanation": "PFR stands for Plug Flow Reactor, characterized by flow in which fluid particles move in the axial direction only, with minimal mixing."
        },
        {
            "question": "Which statement best describes the flow pattern in an ideal PFR?",
            "options": [
                "All fluid elements have the same residence time",
                "Fluid is perfectly mixed throughout the reactor",
                "Backmixing occurs throughout the reactor",
                "Fluid flows in a turbulent pattern"
            ],
            "correct": 0,
            "explanation": "In an ideal PFR, all fluid elements that enter at the same time have identical residence times in the reactor."
        },
        {
            "question": "How does concentration vary along the length of a PFR?",
            "options": [
                "Remains constant",
                "Changes with position",
                "Is uniform throughout",
                "Varies randomly"
            ],
            "correct": 1,
            "explanation": "Reactant concentration varies with position along a PFR, typically decreasing from inlet to outlet as the reaction proceeds."
        },
        {
            "question": "What is the residence time distribution in an ideal PFR?",
            "options": [
                "Exponential decay",
                "Normal distribution",
                "Dirac delta function",
                "Uniform distribution"
            ],
            "correct": 2,
            "explanation": "An ideal PFR has a Dirac delta function as its residence time distribution, meaning all fluid elements have exactly the same residence time."
        },
        {
            "question": "For the same conversion and feed rate, how does the volume of a PFR typically compare to a single CSTR?",
            "options": [
                "PFR requires larger volume",
                "PFR requires smaller volume",
                "Both require the same volume",
                "Depends on the reaction order"
            ],
            "correct": 1,
            "explanation": "For most reactions, a PFR requires less volume than a CSTR to achieve the same conversion, especially for higher-order reactions."
        },
        {
            "question": "The design equation for a PFR with reaction rate -rA is:",
            "options": [
                "V = FA0X/-rA",
                "V = FA0X/(-rA(1-X))",
                "V = FA0∫(dX/-rA)",
                "V = FA0/-rA"
            ],
            "correct": 2,
            "explanation": "The PFR design equation is V = FA0∫(dX/-rA), where the integral is taken from X=0 to X=final conversion."
        },
        {
            "question": "Which type of reactions benefit most from PFR configuration?",
            "options": [
                "Zero-order reactions",
                "First-order reactions",
                "Higher-order reactions",
                "All reaction orders benefit equally"
            ],
            "correct": 2,
            "explanation": "Higher-order reactions benefit most from PFRs because the reaction rate is faster at higher concentrations, which occur at the reactor entrance."
        },
        {
            "question": "What industrial reactor type most closely resembles a PFR?",
            "options": [
                "Stirred tank",
                "Fluidized bed",
                "Tubular reactor",
                "Bubble column"
            ],
            "correct": 2,
            "explanation": "Tubular reactors are the industrial implementation of PFRs, with flow through a cylindrical pipe or tube."
        },
        {
            "question": "For a first-order reaction, how does the concentration profile along a PFR appear?",
            "options": [
                "Linear decrease",
                "Exponential decrease",
                "Parabolic decrease",
                "Step change"
            ],
            "correct": 1,
            "explanation": "For a first-order reaction in a PFR, concentration decreases exponentially along the length of the reactor."
        },
        {
            "question": "What is a potential disadvantage of PFRs compared to CSTRs?",
            "options": [
                "Lower conversion",
                "Higher pressure drop",
                "Lower selectivity",
                "More complex mathematical modeling"
            ],
            "correct": 1,
            "explanation": "PFRs typically have higher pressure drops than CSTRs, especially when packed with catalyst or operating at high flow rates."
        }
    ],
    "crushers": [
        {
            "question": "What is the primary purpose of crushers in chemical engineering?",
            "options": [
                "To mix materials together",
                "To reduce particle size",
                "To separate solids from liquids",
                "To increase material density"
            ],
            "correct": 1,
            "explanation": "Crushers are primarily used to reduce the size of large solid materials into smaller pieces."
        },
        {
            "question": "Which of the following is NOT a common type of crusher?",
            "options": [
                "Jaw crusher",
                "Gyratory crusher",
                "Impact crusher",
                "Distillation crusher"
            ],
            "correct": 3,
            "explanation": "Distillation crusher is not a type of crusher. Distillation is a separation process, not a size reduction technique."
        },
        {
            "question": "What is the crushing ratio typically defined as?",
            "options": [
                "The ratio of feed rate to product rate",
                "The ratio of feed size to product size",
                "The ratio of crusher power to throughput",
                "The ratio of crusher volume to material volume"
            ],
            "correct": 1,
            "explanation": "Crushing ratio is defined as the ratio of the feed particle size to the product particle size, indicating how much size reduction occurs."
        },
        {
            "question": "Which law states that the energy required for size reduction is proportional to the new surface area created?",
            "options": [
                "Kick's Law",
                "Rittinger's Law",
                "Bond's Law",
                "Newton's Law"
            ],
            "correct": 1,
            "explanation": "Rittinger's Law states that the energy required for size reduction is proportional to the new surface area created during the process."
        },
        {
            "question": "What is the primary mechanism of size reduction in a ball mill?",
            "options": [
                "Compression",
                "Impact and attrition",
                "Cutting",
                "Shearing"
            ],
            "correct": 1,
            "explanation": "Ball mills reduce particle size primarily through impact (balls striking particles) and attrition (rubbing action between particles)."
        },
        {
            "question": "Which crusher is most suitable for very hard materials in primary crushing operations?",
            "options": [
                "Hammer mill",
                "Jaw crusher",
                "Roller mill",
                "Disk attrition mill"
            ],
            "correct": 1,
            "explanation": "Jaw crushers are commonly used for primary crushing of very hard materials due to their robust design and high crushing force."
        },
        {
            "question": "What is the critical speed of a ball mill?",
            "options": [
                "The speed at which maximum grinding occurs",
                "The speed at which balls begin to centrifuge against the mill wall",
                "The minimum speed required for effective grinding",
                "The speed at which the mill bearings fail"
            ],
            "correct": 1,
            "explanation": "Critical speed is when centrifugal force balances gravity, causing balls to centrifuge against the mill wall rather than falling to create impact."
        },
        {
            "question": "Which equation most accurately represents Bond's Law for crushing energy?",
            "options": [
                "E = K(1/P - 1/F)",
                "E = K log(F/P)",
                "E = K(1/√P - 1/√F)",
                "E = K(F-P)"
            ],
            "correct": 2,
            "explanation": "Bond's Law states that the energy required is proportional to the difference in the reciprocals of the square roots of the product and feed sizes: E = K(1/√P - 1/√F)."
        },
        {
            "question": "What is the most common method to describe particle size distribution from crushers?",
            "options": [
                "Normal distribution",
                "Poisson distribution",
                "Exponential distribution",
                "Log-normal distribution"
            ],
            "correct": 3,
            "explanation": "Particle size distributions from crushing and grinding operations typically follow a log-normal distribution pattern."
        },
        {
            "question": "Which factor does NOT significantly affect ball mill performance?",
            "options": [
                "Mill rotation speed",
                "Ball size and density",
                "Mill loading",
                "Ambient air temperature"
            ],
            "correct": 3,
            "explanation": "Ambient air temperature generally has minimal effect on ball mill performance compared to operational parameters like speed, ball characteristics, and loading."
        }
    ],
    "filter_press": [
        {
            "question": "What is the primary function of a plate and frame filter press?",
            "options": [
                "To mix solids and liquids",
                "To separate solids from liquids",
                "To reduce particle size",
                "To increase liquid temperature"
            ],
            "correct": 1,
            "explanation": "A plate and frame filter press is primarily used to separate solids from liquids by forcing the liquid through a filter medium while retaining the solids."
        },
        {
            "question": "In a filter press, the filter cake forms on:",
            "options": [
                "The plates",
                "The frames",
                "The filter cloth",
                "The hydraulic system"
            ],
            "correct": 2,
            "explanation": "The filter cake forms on the filter cloth as the liquid passes through, leaving solid particles behind."
        },
        {
            "question": "Which equation correctly represents the basic filtration equation for constant pressure filtration?",
            "options": [
                "t/V = αμcV/2A²P + μRm/AP",
                "t/V = αμc/2A²P + μRm/AP",
                "t/V = αμcV/2A²P",
                "t/V = μRm/AP"
            ],
            "correct": 0,
            "explanation": "The correct equation for constant pressure filtration is t/V = αμcV/2A²P + μRm/AP, relating time, volume, and filtration parameters."
        },
        {
            "question": "What is the filter medium resistance (Rm) in filtration theory?",
            "options": [
                "The resistance of the cake to filtration",
                "The resistance of the liquid to flow",
                "The initial resistance of the clean filter medium",
                "The resistance of the filter press frame"
            ],
            "correct": 2,
            "explanation": "Filter medium resistance (Rm) is the initial resistance offered by the clean filter medium before any cake has formed."
        },
        {
            "question": "What is typically plotted to determine specific cake resistance (α) for constant pressure filtration?",
            "options": [
                "t vs. V",
                "t/V vs. V",
                "t vs. t/V",
                "V vs. P"
            ],
            "correct": 1,
            "explanation": "Plotting t/V vs. V yields a straight line with slope related to specific cake resistance and y-intercept related to medium resistance."
        },
        {
            "question": "Which parameter most significantly affects filtration rate in a filter press?",
            "options": [
                "Filter medium color",
                "Applied pressure",
                "Ambient temperature",
                "Frame material"
            ],
            "correct": 1,
            "explanation": "Applied pressure is a key parameter affecting filtration rate, with higher pressures generally resulting in faster filtration."
        },
        {
            "question": "How does cake compressibility affect the specific cake resistance in filtration?",
            "options": [
                "Compressible cakes have constant resistance regardless of pressure",
                "Compressible cakes have lower resistance at higher pressures",
                "Compressible cakes have higher resistance at higher pressures",
                "Cake compressibility has no effect on resistance"
            ],
            "correct": 2,
            "explanation": "For compressible cakes, specific cake resistance increases with pressure as the cake compresses and becomes less permeable."
        },
        {
            "question": "What is the wash ratio in filter press operations?",
            "options": [
                "The ratio of wash liquid to filtrate volume",
                "The ratio of cake volume to frame volume",
                "The ratio of filtration time to washing time",
                "The ratio of solids to liquid in the slurry"
            ],
            "correct": 0,
            "explanation": "Wash ratio is the volume of wash liquid used relative to the volume of filtrate, indicating washing efficiency."
        },
        {
            "question": "Which of the following is an advantage of filter presses over continuous filters?",
            "options": [
                "Higher throughput",
                "Lower labor requirements",
                "Ability to handle high solids concentration",
                "Lower capital cost"
            ],
            "correct": 2,
            "explanation": "Filter presses can handle slurries with high solids concentrations and produce drier cakes compared to many continuous filters."
        },
        {
            "question": "What is the recommended approach for filtering slurries with very fine particles?",
            "options": [
                "Increase filtration pressure only",
                "Use coarser filter media",
                "Add filter aids such as diatomaceous earth",
                "Decrease slurry concentration"
            ],
            "correct": 2,
            "explanation": "Filter aids like diatomaceous earth create more permeable cake structures, improving filtration of fine particles that might otherwise clog the filter medium."
        }
    ],
    "rotary_vacuum_filter": [
        {
            "question": "What is the main working principle of a rotary vacuum filter?",
            "options": [
                "Centrifugal force separates solids from liquids",
                "Vacuum draws liquid through a filter medium while solids form a cake",
                "Pressure forces liquid through a filter medium",
                "Gravity separates particles of different densities"
            ],
            "correct": 1,
            "explanation": "Rotary vacuum filters operate by applying vacuum to draw liquid through a filter medium on a rotating drum, leaving solids as a cake on the surface."
        },
        {
            "question": "What is the typical arrangement of a rotary vacuum filter drum?",
            "options": [
                "Vertical axis of rotation",
                "Horizontal axis of rotation with drum fully submerged",
                "Horizontal axis of rotation with drum partially submerged",
                "Inclined axis of rotation"
            ],
            "correct": 2,
            "explanation": "The drum typically rotates around a horizontal axis and is partially submerged in the slurry, with sections for cake formation, washing, drying, and discharge."
        },
        {
            "question": "Which of the following is NOT a common zone in a rotary vacuum filter operation?",
            "options": [
                "Cake formation zone",
                "Washing zone",
                "Drying zone",
                "Heating zone"
            ],
            "correct": 3,
            "explanation": "Standard zones include cake formation (submergence), washing, drying, and discharge. A dedicated heating zone is not standard."
        },
        {
            "question": "What is the function of the doctor blade in a rotary vacuum filter?",
            "options": [
                "To spread the slurry evenly",
                "To wash the filter cake",
                "To remove the filter cake from the drum",
                "To monitor filtration quality"
            ],
            "correct": 2,
            "explanation": "The doctor blade (or knife) scrapes the filter cake off the drum surface at the discharge point."
        },
        {
            "question": "How is vacuum typically maintained in different zones of a rotary vacuum filter?",
            "options": [
                "Through a stationary valve head at one end of the drum",
                "Through individual vacuum pumps for each zone",
                "Through holes drilled directly into the drum surface",
                "Through a central shaft within the drum"
            ],
            "correct": 0,
            "explanation": "A stationary valve head (or rotary valve) at one end of the drum connects different sections to vacuum or pressure as the drum rotates."
        },
        {
            "question": "What determines the optimal drum submergence in a rotary vacuum filter?",
            "options": [
                "Desired cake thickness only",
                "Filtration rate only",
                "Balance between cake formation rate and rotation speed",
                "Slurry temperature"
            ],
            "correct": 2,
            "explanation": "Submergence is optimized to balance cake formation rate and rotation speed, ensuring adequate cake thickness without excessive submergence time."
        },
        {
            "question": "Which parameter has the most significant effect on the capacity of a rotary vacuum filter?",
            "options": [
                "Drum diameter",
                "Drum length",
                "Filtration area",
                "Drum material"
            ],
            "correct": 2,
            "explanation": "The total filtration area (which depends on both diameter and length) is the most significant parameter affecting capacity."
        },
        {
            "question": "What is the primary advantage of rotary vacuum filters over batch filters like filter presses?",
            "options": [
                "Higher filtration pressures",
                "Continuous operation",
                "Better cake washing",
                "Lower energy consumption"
            ],
            "correct": 1,
            "explanation": "The primary advantage is continuous operation, allowing for uninterrupted processing of slurries without the cycle times of batch filters."
        },
        {
            "question": "Which factor does NOT significantly affect cake formation in a rotary vacuum filter?",
            "options": [
                "Vacuum level",
                "Drum rotation speed",
                "Slurry concentration",
                "Ambient air humidity"
            ],
            "correct": 3,
            "explanation": "Ambient air humidity generally has minimal impact on cake formation compared to operational parameters like vacuum level, rotation speed, and slurry characteristics."
        },
        {
            "question": "What is the typical range of drum rotation speeds for rotary vacuum filters?",
            "options": [
                "0.1-1 rpm",
                "1-5 rpm",
                "10-50 rpm",
                "100-200 rpm"
            ],
            "correct": 1,
            "explanation": "Rotary vacuum filters typically operate at relatively slow speeds, usually in the range of 1-5 rpm, to allow adequate time for cake formation and processing."
        }
    ],
    "centrifuge_flotation": [
        {
            "question": "What is the main separation principle in a centrifuge?",
            "options": [
                "Filtration",
                "Centrifugal force",
                "Flotation",
                "Adsorption"
            ],
            "correct": 1,
            "explanation": "Centrifuges separate materials based on density differences using centrifugal force, which acts as an enhanced gravitational field."
        },
        {
            "question": "What is the primary driving force in flotation separation?",
            "options": [
                "Density difference",
                "Surface property differences (hydrophobicity/hydrophilicity)",
                "Particle size",
                "Magnetic properties"
            ],
            "correct": 1,
            "explanation": "Flotation separates particles based on differences in surface properties, specifically the hydrophobicity of particles that attach to air bubbles."
        },
        {
            "question": "Which of the following is NOT a common type of industrial centrifuge?",
            "options": [
                "Disc stack centrifuge",
                "Decanter centrifuge",
                "Basket centrifuge",
                "Flotation centrifuge"
            ],
            "correct": 3,
            "explanation": "Flotation centrifuge is not a standard type. Flotation and centrifugation are different separation processes."
        },
        {
            "question": "What is the role of frothers in flotation?",
            "options": [
                "To make minerals hydrophobic",
                "To stabilize air bubbles and froth",
                "To depress unwanted minerals",
                "To increase pulp density"
            ],
            "correct": 1,
            "explanation": "Frothers are surfactants that stabilize air bubbles and the froth layer, preventing bubbles from coalescing or breaking too quickly."
        },
        {
            "question": "The separation factor in centrifugation is defined as:",
            "options": [
                "The ratio of centrifugal force to gravitational force",
                "The ratio of feed rate to product rate",
                "The ratio of separated material to total material",
                "The ratio of rotation speed to critical speed"
            ],
            "correct": 0,
            "explanation": "The separation factor (G-force) is the ratio of centrifugal acceleration to gravitational acceleration, indicating how much stronger the separation force is compared to gravity."
        },
        {
            "question": "Which equation correctly describes the settling velocity of a particle in a centrifuge?",
            "options": [
                "v = d²(ρₚ-ρₗ)ω²r/18μ",
                "v = d²(ρₚ-ρₗ)g/18μ",
                "v = d(ρₚ-ρₗ)ω²r/18μ",
                "v = d²(ρₚ-ρₗ)ω²/18μ"
            ],
            "correct": 0,
            "explanation": "The settling velocity in a centrifuge is proportional to particle diameter squared, density difference, angular velocity squared, and radial position."
        },
        {
            "question": "What is the primary function of collectors in flotation?",
            "options": [
                "To create stable froth",
                "To make mineral surfaces hydrophobic",
                "To increase pulp density",
                "To clean the flotation cell"
            ],
            "correct": 1,
            "explanation": "Collectors are reagents that selectively adsorb onto mineral surfaces, rendering them hydrophobic so they can attach to air bubbles."
        },
        {
            "question": "Which centrifuge type is most suitable for separating two liquid phases with a small amount of solids?",
            "options": [
                "Tubular bowl centrifuge",
                "Disc stack centrifuge",
                "Decanter centrifuge",
                "Basket centrifuge"
            ],
            "correct": 1,
            "explanation": "Disc stack centrifuges are well-suited for liquid-liquid separation with small amounts of solids due to their high separation efficiency and continuous operation."
        },
        {
            "question": "What is the role of depressants in flotation circuits?",
            "options": [
                "To enhance the flotation of valuable minerals",
                "To prevent specific minerals from floating",
                "To stabilize the froth",
                "To increase recovery"
            ],
            "correct": 1,
            "explanation": "Depressants selectively prevent certain minerals from floating by making or keeping their surfaces hydrophilic, improving separation selectivity."
        },
        {
            "question": "Which parameter is most important in determining the capacity of a centrifuge?",
            "options": [
                "Bowl diameter",
                "Bowl length",
                "Rotation speed",
                "All of the above"
            ],
            "correct": 3,
            "explanation": "Centrifuge capacity depends on all these factors: bowl dimensions determine volume, while rotation speed affects separation efficiency and throughput capability."
        }
    ],
    "classifiers": [
        {
            "question": "What is the primary purpose of a classifier in mineral processing?",
            "options": [
                "To crush large particles",
                "To separate particles based on size, shape, or density",
                "To mix different mineral streams",
                "To change the chemical composition of particles"
            ],
            "correct": 1,
            "explanation": "Classifiers separate particles based on physical properties like size, shape, or density, often using fluid dynamics principles."
        },
        {
            "question": "Which principle is primarily used in hydraulic classifiers?",
            "options": [
                "Centrifugal separation",
                "Differential settling velocities in a fluid",
                "Magnetic properties",
                "Electrical conductivity"
            ],
            "correct": 1,
            "explanation": "Hydraulic classifiers use differences in particle settling velocities in a fluid, which depend on particle size, shape, and density."
        },
        {
            "question": "What is the main separation mechanism in a cone classifier?",
            "options": [
                "Centrifugal force",
                "Hindered settling",
                "Filtration",
                "Flocculation"
            ],
            "correct": 1,
            "explanation": "Cone classifiers use hindered settling, where particle beds form with coarser particles settling faster than finer ones."
        },
        {
            "question": "In a thickener, what is the primary purpose?",
            "options": [
                "To separate solids by size",
                "To increase the solids concentration in slurry",
                "To filter out impurities",
                "To classify particles by density"
            ],
            "correct": 1,
            "explanation": "Thickeners primarily increase the solids concentration in a slurry by allowing solids to settle and removing clarified liquid overflow."
        },
        {
            "question": "Stokes' Law is applicable to which regime of particle settling?",
            "options": [
                "Turbulent flow regime",
                "Laminar flow regime",
                "Transitional flow regime",
                "All flow regimes"
            ],
            "correct": 1,
            "explanation": "Stokes' Law applies only in the laminar flow regime, typically for small particles with Reynolds numbers less than 0.3."
        },
        {
            "question": "The terminal settling velocity of a particle in a fluid is directly proportional to:",
            "options": [
                "Particle diameter",
                "Square of particle diameter",
                "Cube of particle diameter",
                "Square root of particle diameter"
            ],
            "correct": 1,
            "explanation": "According to Stokes' Law, terminal settling velocity is proportional to the square of particle diameter in the laminar flow regime."
        },
        {
            "question": "What is the cut size (d50) in classification?",
            "options": [
                "The maximum particle size in the feed",
                "The minimum particle size in the feed",
                "The particle size reporting equally to both overflow and underflow",
                "The average particle size of the feed"
            ],
            "correct": 2,
            "explanation": "The cut size (d50) is the particle size that has an equal probability of reporting to either the overflow or underflow stream."
        },
        {
            "question": "Which parameter is most important in determining thickener area requirements?",
            "options": [
                "Slurry density",
                "Settling flux",
                "Overflow clarity",
                "Underflow solids concentration"
            ],
            "correct": 1,
            "explanation": "Settling flux (mass settling rate per unit area) is the primary parameter for determining the required thickener area."
        },
        {
            "question": "What is the effect of flocculants in a thickener?",
            "options": [
                "They increase particle size by aggregation",
                "They decrease settling rate",
                "They increase slurry viscosity only",
                "They disperse particles more uniformly"
            ],
            "correct": 0,
            "explanation": "Flocculants cause fine particles to aggregate into larger flocs, increasing effective particle size and settling velocity."
        },
        {
            "question": "Which of the following will increase the efficiency of a hydrocyclone classifier?",
            "options": [
                "Increasing feed solids concentration",
                "Decreasing feed pressure",
                "Increasing cyclone diameter",
                "Decreasing vortex finder diameter"
            ],
            "correct": 3,
            "explanation": "Decreasing the vortex finder diameter generally increases classification efficiency by directing more fine particles to the overflow."
        }
    ],
    "trommel": [
        {
            "question": "What is a trommel screen primarily used for?",
            "options": [
                "Crushing material",
                "Screening/classifying material by size",
                "Washing material",
                "Mixing different materials"
            ],
            "correct": 1,
            "explanation": "A trommel screen is primarily used for separating materials based on particle size using a rotating perforated drum."
        },
        {
            "question": "What is the basic structure of a trommel screen?",
            "options": [
                "A stationary flat screen with vibrating mechanism",
                "A rotating cylindrical drum with perforations",
                "A series of stacked horizontal screens",
                "A conical vessel with internal spirals"
            ],
            "correct": 1,
            "explanation": "A trommel consists of a rotating cylindrical drum with perforations or screen openings of specific sizes."
        },
        {
            "question": "How does material typically move through a trommel screen?",
            "options": [
                "By forced air pressure",
                "By gravity and the rotating action of the drum",
                "By mechanical conveyors inside the drum",
                "By hydraulic flow"
            ],
            "correct": 1,
            "explanation": "Material moves through a trommel via gravity and the lifting/tumbling action created by the drum's rotation."
        },
        {
            "question": "Which factor most significantly affects the screening efficiency of a trommel?",
            "options": [
                "Drum material",
                "Ambient temperature",
                "Rotational speed",
                "Drum color"
            ],
            "correct": 2,
            "explanation": "Rotational speed significantly affects efficiency by influencing material residence time and tumbling action."
        },
        {
            "question": "What is the purpose of lifters often installed inside trommel screens?",
            "options": [
                "To increase drum structural integrity",
                "To lift and tumble material for better screening",
                "To reduce noise during operation",
                "To prevent screen blinding"
            ],
            "correct": 1,
            "explanation": "Lifters raise material and cause it to tumble as the drum rotates, improving exposure to screen openings."
        },
        {
            "question": "In a trommel with multiple screen sections, how are the sections typically arranged?",
            "options": [
                "Random screen sizes",
                "Largest openings first, progressing to smallest",
                "Smallest openings first, progressing to largest",
                "Alternate between large and small openings"
            ],
            "correct": 1,
            "explanation": "Trommels typically arrange screens with largest openings at the feed end, progressing to smaller openings to efficiently remove oversize material first."
        },
        {
            "question": "What is the cut size of a trommel screen?",
            "options": [
                "The largest particle that can enter the trommel",
                "The size of the screen openings",
                "The smallest particle retained by the screen",
                "The average size of feed material"
            ],
            "correct": 1,
            "explanation": "The cut size is defined by the screen opening size, which determines what passes through versus what is retained."
        },
        {
            "question": "Which of the following is a common application for trommel screens?",
            "options": [
                "Municipal waste sorting",
                "Liquid filtration",
                "Gas separation",
                "Chemical synthesis"
            ],
            "correct": 0,
            "explanation": "Trommel screens are commonly used in waste management for separating different sized fractions in municipal solid waste."
        },
        {
            "question": "What is screen blinding in a trommel?",
            "options": [
                "When the drum rotates too fast for visual inspection",
                "When the screen openings become blocked or clogged with material",
                "When the screen breaks due to excessive load",
                "When the material becomes too wet to screen effectively"
            ],
            "correct": 1,
            "explanation": "Screen blinding occurs when apertures become clogged with near-size or sticky particles, reducing screening efficiency."
        },
        {
            "question": "Which parameter is used to express trommel screening performance?",
            "options": [
                "Screening time only",
                "Drum diameter only",
                "Screening efficiency or recovery",
                "Material density only"
            ],
            "correct": 2,
            "explanation": "Screening efficiency or recovery (percentage of undersize material that correctly passes through the screen) is a key performance metric."
        }
    ]
}

def run_quiz(experiment_name):
    """Run a quiz for the specified experiment"""
    st.title(f"Quiz: {experiment_name.replace('_', ' ').title()}")
    
    # Check if we have questions for this experiment
    if experiment_name not in quiz_questions:
        st.error(f"No quiz questions available for {experiment_name}")
        return
    
    # Initialize session state for quiz if not already done
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'selected_questions' not in st.session_state:
        # Select 2 random questions initially
        available_questions = quiz_questions[experiment_name]
        if len(available_questions) < 2:
            st.warning("Not enough questions available for this quiz.")
            st.session_state.selected_questions = available_questions
        else:
            st.session_state.selected_questions = random.sample(available_questions, 2)
    if 'answers' not in st.session_state:
        st.session_state.answers = [-1] * len(st.session_state.selected_questions)
        
    # Use the stored questions
    selected_questions = st.session_state.selected_questions
    
    # Display introduction and instructions
    st.markdown("""
    This quiz will test your understanding of the concepts related to this experiment.
    Select the correct answer for each question and submit your answers to see your score.
    """)
    
    # Display the selected questions
    for i, q in enumerate(selected_questions):
        st.subheader(f"Question {i+1}")
        st.write(q["question"])
        
        # Create a unique key for each radio button
        key = f"q{i}"
        
        # Display options
        st.session_state.answers[i] = st.radio(
            "Select your answer:",
            options=range(len(q["options"])),
            format_func=lambda x: q["options"][x],
            key=key,
            index=st.session_state.answers[i] if st.session_state.answers[i] >= 0 else 0
        )
    
    # Submit button
    if st.button("Submit Quiz") or st.session_state.submitted:
        st.session_state.submitted = True
        
        # Calculate score
        correct_count = 0
        for i, q in enumerate(selected_questions):
            user_answer = st.session_state.answers[i]
            correct_answer = q["correct"]
            
            if user_answer == correct_answer:
                correct_count += 1
                st.success(f"Question {i+1}: Correct! {q['explanation']}")
            else:
                st.error(f"Question {i+1}: Incorrect. The correct answer is: {q['options'][correct_answer]}. {q['explanation']}")
        
        # Display score
        st.session_state.score = correct_count
        percentage = (correct_count / len(selected_questions)) * 100
        
        st.markdown(f"### Your Score: {correct_count}/{len(selected_questions)} ({percentage:.1f}%)")
        
        if percentage >= 70:
            st.balloons()
            st.success("Great job! You've demonstrated a good understanding of this topic.")
        else:
            st.info("Keep studying! Review the experiment simulation to better understand the concepts.")
    
    # Reset button to try again with new questions
    if st.session_state.submitted and st.button("Try Again"):
        st.session_state.submitted = False
        # Select new random questions
        available_questions = quiz_questions[experiment_name]
        if len(available_questions) < 2:
            st.session_state.selected_questions = available_questions
        else:
            st.session_state.selected_questions = random.sample(available_questions, 2)
        st.session_state.answers = [-1] * len(st.session_state.selected_questions)
        st.session_state.score = 0
        st.rerun()
    
    # Link back to simulation
    st.markdown("---")
    st.markdown("Return to the simulation to explore this experiment further.")
