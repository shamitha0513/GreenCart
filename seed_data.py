import os
import uuid
from datetime import datetime, timedelta
from app import create_app, db
from app.models import (
    User, Address, Category, Plant, Cart, Order, OrderItem, Payment, 
    DeliveryPartner, Service, ServiceBooking, Review
)

# 12 Categories from PDF Section 8
CATEGORIES_DATA = [
    {"name": "Indoor Plants", "slug": "indoor-plants", "description": "Beautiful, shade-loving plants perfect for enhancing living rooms and office spaces."},
    {"name": "Outdoor Plants", "slug": "outdoor-plants", "description": "Sun-loving shrubs, trees, and foliage plants for garden landscapes and balconies."},
    {"name": "Flowering Plants", "slug": "flowering-plants", "description": "Vibrant and colorful blooming plants to add joy and fragrance to your home."},
    {"name": "Herbal Plants", "slug": "herbal-plants", "description": "Aromatic culinary herbs for fresh kitchen recipes and home remedies."},
    {"name": "Medicinal Plants", "slug": "medicinal-plants", "description": "Traditional healing and wellness plants with natural therapeutic benefits."},
    {"name": "Succulents", "slug": "succulents", "description": "Low-maintenance, drought-tolerant plants with fleshy leaves in gorgeous geometric shapes."},
    {"name": "Air Purifying Plants", "slug": "air-purifying-plants", "description": "NASA-recommended plants that actively filter indoor toxins, dust, and pollutants."},
    {"name": "Ornamental Plants", "slug": "ornamental-plants", "description": "Decorative foliage plants with unique leaf patterns and striking textures."},
    {"name": "Fruit Plants", "slug": "fruit-plants", "description": "Fruit-bearing dwarf trees and plants for home gardening harvest."},
    {"name": "Vegetable Plants", "slug": "vegetable-plants", "description": "Fresh home-growable vegetable and vegetable seedling varieties."},
    {"name": "Cactus Plants", "slug": "cactus-plants", "description": "Desert-adapted spiky plants requiring minimal watering and full sun."},
    {"name": "Bonsai Plants", "slug": "bonsai-plants", "description": "Artistically pruned miniature trees representing peace, patience, and harmony."}
]

# 15 Specific Plants per Category (180 Plants Total)
PLANTS_BY_CATEGORY = {
    "Indoor Plants": [
        ("Snake Plant", "Sansevieria trifasciata", 499, 10, "Low-light survivor with upright sword-like leaves.", "Air purification, releases oxygen at night.", "Water every 2-3 weeks. Indirect light.", "Indirect Sun", "Low Water", "Well-Draining", "Medium"),
        ("Peace Lily", "Spathiphyllum wallisii", 599, 15, "Elegant dark green leaves with graceful white spathe flowers.", "Filters formaldehydes and benzene.", "Keep soil moist, mist leaves periodically.", "Partial Shade", "Medium Water", "Peat Moss Mix", "Medium"),
        ("Monstera Deliciosa", "Monstera deliciosa", 899, 20, "Famous Swiss Cheese plant with iconic split tropical leaves.", "High aesthetic value, air purifier.", "Water when top 2 inches of soil dry.", "Bright Indirect", "Medium Water", "Loamy Mix", "Large"),
        ("ZZ Plant", "Zamioculcas zamiifolia", 649, 10, "Glossy dark green leaves that thrive on minimal care.", "Extremely resilient, cleans air.", "Water sparingly once a month.", "Low Light", "Low Water", "Sandy Loam", "Medium"),
        ("Devil's Ivy Pothos", "Epipremnum aureum", 349, 0, "Fast-growing trailing vine with variegated gold-green leaves.", "Absorbs indoor VOC toxins.", "Water when soil feels dry.", "Adaptable", "Medium Water", "Standard Pot Mix", "Small"),
        ("Chinese Evergreen", "Aglaonema commutatum", 549, 15, "Patterned pink and green lush indoor foliage.", "Tolerates low light and dry air.", "Keep away from cold drafts, water moderately.", "Low Light", "Medium Water", "Rich Organic", "Medium"),
        ("Fiddle Leaf Fig", "Ficus lyrata", 1299, 10, "Large fiddle-shaped leathery leaves for architectural interior design.", "Creates stunning focal point.", "Wipe dust off leaves, keep near window.", "Bright Light", "Weekly Water", "Well-Draining", "Large"),
        ("Rubber Plant", "Ficus elastica", 749, 12, "Deep burgundy glossy leaves that purify indoor air.", "Traps atmospheric dust particles.", "Allow top soil to dry between waterings.", "Bright Indirect", "Medium Water", "Peat-Perlite Mix", "Large"),
        ("Spider Plant", "Chlorophytum comosum", 299, 25, "Arching green leaves with white stripes producing plantlets.", "Removes carbon monoxide and xylene.", "Water twice weekly in summer.", "Partial Sun", "Regular Water", "Garden Soil", "Small"),
        ("Cast Iron Plant", "Aspidistra elatior", 699, 8, "Nearly indestructible foliage plant for shaded corners.", "Resists temperature neglect.", "Water when soil dries out completely.", "Deep Shade", "Low Water", "Universal Mix", "Medium"),
        ("Parlor Palm", "Chamaedorea elegans", 799, 15, "Feathery tropical palm fronds suitable for indoor spaces.", "Increases humidity levels.", "Keep soil evenly moist, never waterlogged.", "Filtered Light", "Moderate Water", "Palm Mix", "Medium"),
        ("Calathea Rattlesnake", "Goeppertia insignis", 629, 18, "Wavy leaves with dark green spots and purple undersides.", "Non-toxic pet safe plant.", "Requires high humidity and distilled water.", "Shade", "High Water", "Peat Perlite", "Small"),
        ("Boston Fern", "Nephrolepis exaltata", 449, 20, "Lush feathery fronds cascading gracefully from pots.", "Natural room humidifier.", "Keep soil moist and mist daily.", "Medium Light", "High Water", "Peat Base", "Medium"),
        ("Anthurium Flamingo", "Anthurium andraeanum", 849, 10, "Heart-shaped glossy leaves with long-lasting red flower spathes.", "Blooms repeatedly year round.", "Needs warmth and high ambient humidity.", "Bright Indirect", "Medium Water", "Orchid Mix", "Small"),
        ("Heartleaf Philodendron", "Philodendron hederaceum", 399, 30, "Charming trailing heart-shaped leaves for hanging baskets.", "Fast growing and low maintenance.", "Trim stems to encourage bushiness.", "Indirect Sun", "Moderate Water", "Potting Soil", "Small")
    ],
    "Outdoor Plants": [
        ("Bougainvillea Pink", "Bougainvillea spectabilis", 499, 15, "Vibrant magenta flowering climber for sunny gates and walls.", "Heat and drought resistant bloom.", "Full direct sunlight, water when soil is dry.", "Full Sun", "Low Water", "Clay Loam", "Large"),
        ("Areca Palm", "Dypsis lutescens", 899, 20, "Feathery clump-forming golden palm for outdoor patios.", "Provides privacy screening.", "Water regularly and fertilize seasonally.", "Full Sun", "Medium Water", "Well-Draining", "Large"),
        ("Hibiscus Red", "Hibiscus rosa-sinensis", 349, 12, "Large tropical red blooms attracting butterflies.", "Continuous floral display.", "Prune regularly for more blooms.", "Full Sun", "Daily Water", "Nutrient Rich", "Medium"),
        ("Ficus Benjamina Tree", "Ficus benjamina", 999, 10, "Graceful weeping fig tree for outdoor garden spaces.", "Excellent hedge or specimen tree.", "Protect from extreme frost.", "Partial Sun", "Moderate Water", "Garden Loam", "Large"),
        ("Ixora Coccinea", "Ixora coccinea", 299, 25, "Dense clusters of bright scarlet star-shaped flowers.", "Great for garden borders.", "Prefers slightly acidic soil.", "Full Sun", "Regular Water", "Acidic Loam", "Small"),
        ("Croton Petra", "Codiaeum variegatum", 449, 18, "Rainbow variegated leaves with gold, orange, and red tones.", "Eye-catching outdoor color accent.", "Needs bright light to maintain leaf colors.", "Bright Sun", "Medium Water", "Rich Compost", "Medium"),
        ("Oleander", "Nerium oleander", 399, 15, "Drought-hardy shrub with fragrant pink flower clusters.", "Tough highway and boundary plant.", "Requires minimal irrigation once established.", "Full Direct Sun", "Very Low Water", "Sandy Soil", "Large"),
        ("Golden Trumpet Vine", "Allamanda cathartica", 479, 10, "Vigorous woody climber with bright yellow trumpet flowers.", "Lush fence cover.", "Provide sturdy trellis support.", "Full Sun", "Daily Water", "Organic Loam", "Large"),
        ("Plumeria Frangipani", "Plumeria rubra", 1199, 8, "Fragrant white-yellow tropical flowers with thick succulent branches.", "Sacred flower tree.", "Water sparingly during dormancy.", "Full Sun", "Low Water", "Dry Sandy", "Large"),
        ("Cycas Revoluta Palm", "Cycas revoluta", 1499, 5, "Sago palm with symmetrical whorl of stiff glossy fronds.", "Ancient prehistoric garden centerpiece.", "Slow growing, avoid overwatering.", "Partial Sun", "Low Water", "Coarse Sand Mix", "Medium"),
        ("Duranta Golden Edge", "Duranta erecta", 249, 30, "Golden foliage shrub used for formal garden hedge borders.", "Easy to shape and trim.", "Prune every few months.", "Full Sun", "Moderate Water", "Loamy Soil", "Medium"),
        ("Tecoma Capensis", "Tecoma capensis", 329, 20, "Cape honeysuckle with orange tubular nectar blooms.", "Attracts hummingbirds.", "Trim back after blooming cycle.", "Full Sun", "Medium Water", "Standard Soil", "Medium"),
        ("Canna Lily Yellow", "Canna indica", 299, 15, "Bold banana-like foliage with upright yellow flower spikes.", "Tropical water edge feature.", "Keep soil consistently damp.", "Full Sun", "High Water", "Wet Loam", "Medium"),
        ("Traveller's Palm", "Ravenala madagascariensis", 1999, 6, "Fan-shaped massive green leaves forming stunning natural arch.", "Architectural landscape specimen.", "Needs ample space to spread fan.", "Full Sun", "High Water", "Rich Deep Soil", "Large"),
        ("Night Jasmine Parijat", "Nyctanthes arbor-tristis", 399, 22, "Divine night-blooming white flowers with orange stems.", "Aromatic night garden fragrance.", "Sunlight during day, water regularly.", "Full Sun", "Regular Water", "Garden Soil", "Medium")
    ],
    "Flowering Plants": [
        ("Red Rose Bush", "Rosa rubiginosa", 399, 20, "Classic fragrant velvet red roses blooming continuously.", "Symbol of romance and elegance.", "Prune dead heads, fertilize monthly.", "Full Sun", "Daily Water", "Clay Loam", "Medium"),
        ("Jasmine Jasmine", "Jasminum officinale", 299, 25, "Sweetly scented white star flowers beloved for fragrance.", "Natural essential oil plant.", "Provide fence or stake support.", "Full Sun", "Regular Water", "Rich Organic", "Medium"),
        ("Orchid Phalaenopsis", "Phalaenopsis orchid", 1199, 8, "Exotic long-lasting pink orchid blooms on arching stems.", "Premium luxury gift flower.", "Water pine bark substrate once a week.", "Filtered Light", "Weekly Water", "Orchid Bark", "Small"),
        ("Marigold Orange", "Tagetes erecta", 149, 40, "Bright golden orange festive flower heads.", "Natural pest deterrent in gardens.", "Pinch tips for bushier growth.", "Full Sun", "Moderate Water", "Garden Soil", "Small"),
        ("Dahlia Mixed", "Dahlia hortensis", 349, 15, "Intricate geometric petaled flowers in vibrant colors.", "Showstopping garden bed display.", "Stake tall stems to support blooms.", "Full Sun", "Regular Water", "Rich Loam", "Medium"),
        ("Zinnia Elegans", "Zinnia elegans", 199, 30, "Daisy-like bright flowers blooming non-stop all summer.", "Easy to grow from seed.", "Water at base to avoid leaf mildew.", "Full Sun", "Moderate Water", "Well-Draining", "Small"),
        ("Petunia Mixed", "Petunia hybrida", 179, 35, "Trumpet-shaped colorful cascading blooms for balcony boxes.", "Prolific flowering cover.", "Remove faded flowers to prolong blooming.", "Full Sun", "Daily Water", "Light Mix", "Small"),
        ("Carnation Pink", "Dianthus caryophyllus", 299, 20, "Fragrant ruffled edge pink flowers.", "Excellent cut flower arrangements.", "Keep soil moist but not soggy.", "Partial Sun", "Regular Water", "Neutral Soil", "Small"),
        ("Gerbera Daisy", "Gerbera jamesonii", 399, 18, "Large bright daisy blooms on sturdy leafless stems.", "Radiant indoor or outdoor floral display.", "Protect crown from excess water.", "Bright Sun", "Moderate Water", "Sandy Loam", "Small"),
        ("Chrysanthemum Yellow", "Chrysanthemum morifolium", 279, 22, "Golden autumnal mum flowers with lush dense petals.", "Long blooming period.", "Water soil directly, keep leaves dry.", "Full Sun", "Regular Water", "Compost Rich", "Small"),
        ("Verbena Purple", "Verbena tenera", 229, 25, "Low trailing carpet of rich violet flower clusters.", "Groundcover floral blanket.", "Tolerates heat and bright sunshine.", "Full Sun", "Medium Water", "Sandy Soil", "Small"),
        ("Adenium Desert Rose", "Adenium obesum", 799, 10, "Swollen trunk bonsai succulent with hot pink flowers.", "Unique swollen caudex floral specimen.", "Water sparingly, high light lover.", "Full Sun", "Low Water", "Cactus Mix", "Small"),
        ("Balsam Impatiens", "Impatiens balsamina", 169, 30, "Rosette blooms along succulent fleshy stalks.", "Shade garden bloomer.", "Requires shaded cool soil.", "Shade", "High Water", "Moist Organic", "Small"),
        ("Periwinkle Vinca", "Catharanthus roseus", 149, 45, "Five-petaled tough flower blooming in extreme heat.", "Resilient groundcover.", "Minimal maintenance required.", "Full Sun", "Low Water", "Any Soil", "Small"),
        ("Crossandra Firecracker", "Crossandra infundibuliformis", 249, 20, "Shiny leaves with fan-shaped salmon orange flowers.", "Traditional tropical garland flower.", "Keep moist in warm weather.", "Partial Shade", "Regular Water", "Peat Rich", "Small")
    ],
    "Herbal Plants": [
        ("Sweet Basil", "Ocimum basilicum", 199, 30, "Aromatic green basil leaves essential for Italian pesto and pasta.", "Fresh culinary herb, antibacterial.", "Pinch top leaves for bushy growth.", "Full Sun", "Daily Water", "Rich Loam", "Small"),
        ("Mint Pudina", "Mentha spicata", 149, 40, "Cool refreshing mint leaves for beverages, chutneys, and teas.", "Aids digestion, ultra fast spreading.", "Keep soil damp in containers.", "Partial Sun", "High Water", "Moist Soil", "Small"),
        ("Rosemary", "Salvia rosmarinus", 349, 15, "Woody perennial herb with needle-like fragrant foliage.", "Flavoring roasts, improves memory.", "Allow soil to dry out between waterings.", "Full Sun", "Low Water", "Gritty Sandy", "Medium"),
        ("Thyme German", "Thymus vulgaris", 299, 20, "Tiny aromatic leaves with earthy oregano notes.", "Culinary seasoning, antiseptic.", "Needs bright light and sharp drainage.", "Full Sun", "Low Water", "Dry Sandy", "Small"),
        ("Oregano", "Origanum vulgare", 279, 22, "Pungent Mediterranean herb vital for pizzas and marinadas.", "Antioxidant rich cooking herb.", "Trim regularly before flowering.", "Full Sun", "Low Water", "Poor Soil", "Small"),
        ("Parsley Italian", "Petroselinum crispum", 199, 25, "Flat leaf green parsley packed with Vitamin C.", "Garnish and salad flavoring.", "Keep soil consistently damp.", "Partial Sun", "Regular Water", "Moist Loam", "Small"),
        ("Coriander Cilantro", "Coriandrum sativum", 129, 50, "Fresh tangy cilantro leaves and coriander seeds.", "Essential Asian and Mexican herb.", "Sow seeds repeatedly for continuous harvest.", "Full Sun", "Daily Water", "Standard Mix", "Small"),
        ("Sage Garden", "Salvia officinalis", 329, 12, "Soft silvery green velvet leaves for savory cooking.", "Throat soothe tea, culinary spice.", "Do not overwater soil.", "Full Sun", "Low Water", "Sandy Clay", "Small"),
        ("Lemongrass", "Cymbopogon citratus", 249, 30, "Tall citrus-scented stalks for herbal teas and Thai curries.", "Insect repellent, detoxifying tea.", "Loves heat and generous watering.", "Full Sun", "High Water", "Deep Loam", "Large"),
        ("Curry Leaf Plant", "Murraya koenigii", 299, 18, "Highly aromatic green leaves key to Indian tempering.", "Enhances digestion and hair growth.", "Prune top shoot to encourage branching.", "Full Sun", "Regular Water", "Red Soil", "Medium"),
        ("Chives Garlic", "Allium tuberosum", 179, 28, "Slender onion-flavored green stalks with purple blooms.", "Mild garlic flavor garnish.", "Snip stems from outer edge.", "Full Sun", "Medium Water", "Moist Soil", "Small"),
        ("Dill Herb", "Anethum graveolens", 189, 20, "Feathery green leaves for pickles, soups, and seafood.", "Calms digestive system.", "Protect tall slender stems from wind.", "Full Sun", "Regular Water", "Light Loam", "Medium"),
        ("Marjoram Sweet", "Origanum majorana", 259, 15, "Mild citrusy sweet herb closely related to oregano.", "Soothing herbal infusions.", "Well drained pot location.", "Full Sun", "Low Water", "Sandy Loam", "Small"),
        ("Tarragon French", "Artemisia dracunculus", 399, 10, "Anise-flavored delicate leaves for French sauces.", "Gourmet culinary herb.", "Protect roots from waterlogging.", "Partial Sun", "Moderate Water", "Dry Soil", "Small"),
        ("Stevia Sugar Plant", "Stevia rebaudiana", 299, 15, "Naturally sweet green leaves 300x sweeter than sugar.", "Zero-calorie natural sweetener.", "Pinch flower buds to maintain leaf sweetness.", "Full Sun", "Regular Water", "Organic Mix", "Small")
    ],
    "Medicinal Plants": [
        ("Aloe Vera Gel Plant", "Aloe barbadensis miller", 299, 25, "Thick succulent leaves filled with soothing healing gel.", "Soothes burns, skin care, digestion.", "Water deeply once every 3 weeks.", "Bright Light", "Very Low Water", "Cactus Mix", "Medium"),
        ("Holy Basil Tulsi", "Ocimum sanctum", 199, 50, "Revered sacred herb with powerful immunity-boosting properties.", "Adaptogen, relieves cough and cold.", "Water daily in morning, place in sun.", "Full Sun", "Daily Water", "Sacred Loam", "Medium"),
        ("Ashwagandha", "Withania somnifera", 349, 15, "Indian Ginseng root plant known for vitality and stress relief.", "Reduces anxiety and boosts vigor.", "Water moderately, warm sunny spot.", "Full Sun", "Low Water", "Dry Sandy", "Medium"),
        ("Giloy Amrita", "Tinospora cordifolia", 249, 20, "Heart-leaved climber famous for boosting platelet counts.", "Immunity enhancer against fevers.", "Provide climber lattice support.", "Partial Sun", "Moderate Water", "Garden Soil", "Large"),
        ("Neem Tree Sapling", "Azadirachta indica", 399, 12, "Famed miracle tree with powerful antibacterial and antifungal leaves.", "Purifies skin and air.", "Plant outdoors in spacious sunny area.", "Full Sun", "Low Water", "Hardy Clay", "Large"),
        ("Brahmi Memory Herb", "Bacopa monnieri", 229, 30, "Creeping wetland herb celebrated for brain health and memory.", "Enhances cognitive focus.", "Keep soil moist to wet at all times.", "Partial Sun", "High Water", "Muddy Wet", "Small"),
        ("Insulin Plant", "Costus igneus", 399, 18, "Foliage plant whose leaves help regulate blood glucose levels.", "Traditional diabetes management.", "Water daily, prefers shade.", "Partial Shade", "Daily Water", "Humus Rich", "Medium"),
        ("Gotu Kola", "Centella asiatica", 199, 35, "Fan-shaped creeping leaves for longevity and skin repair.", "Promotes collagen synthesis.", "Loves damp marshy potting soil.", "Partial Shade", "High Water", "Moist Soil", "Small"),
        ("Lemongrass Herbal", "Cymbopogon flexuosus", 249, 25, "Stalks containing essential oil citral for soothing tea.", "Relieves headache and fever.", "Water generously in sunshine.", "Full Sun", "High Water", "Loamy Soil", "Large"),
        ("Shatavari", "Asparagus racemosus", 449, 10, "Feathery climbing plant with tuberous tonic roots.", "Female reproductive health tonic.", "Well draining deep pot.", "Partial Sun", "Moderate Water", "Sandy Clay", "Large"),
        ("Adhatoda Vasa", "Justicia adhatoda", 299, 15, "Medicinal shrub whose leaves clear respiratory congestion.", "Ayurvedic cough remedy.", "Prune annually after monsoon.", "Full Sun", "Regular Water", "Loam Soil", "Medium"),
        ("Stevia Medicinal", "Stevia rebaudiana", 299, 20, "Leaves used as natural low-glycemic sweetener.", "Healthy sugar substitute.", "Do not allow soil to dry completely.", "Full Sun", "Regular Water", "Rich Mix", "Small"),
        ("Vetiver Khus Grass", "Chrysopogon zizanioides", 279, 15, "Deep-rooted fragrant grass used for cooling mats and essential oils.", "Cools body, soil erosion control.", "Water regularly in hot sun.", "Full Sun", "Regular Water", "Deep Soil", "Large"),
        ("Mint Menthol", "Mentha arvensis", 149, 40, "High menthol cooling herb for pain relief balms.", "Soothes stomach and headache.", "Grow in wide shallow pot.", "Partial Sun", "High Water", "Damp Soil", "Small"),
        ("Kalmegh King of Bitters", "Andrographis paniculata", 249, 20, "Bitter tasting herb famous for liver detox and antiviral defense.", "Protects liver function.", "Low maintenance sunny growing.", "Full Sun", "Moderate Water", "Well-Draining", "Small")
    ],
    "Succulents": [
        ("Echeveria Elegans", "Echeveria elegans", 299, 20, "Mexican Snow Rose with tight blue-gray fleshy rosettes.", "Stunning desk accent.", "Water only when soil is completely dry.", "Bright Light", "Low Water", "Cactus Mix", "Small"),
        ("Jade Plant", "Crassula ovata", 399, 15, "Classic Money Tree with thick glossy teardrop leaves.", "Attracts positive energy and wealth.", "Water once every 2 weeks.", "Bright Sun", "Low Water", "Coarse Sandy", "Medium"),
        ("Zebra Haworthia", "Haworthiopsis attenuata", 349, 12, "Dark green pointed leaves with raised white zebra stripes.", "Perfect window-sill plant.", "Tolerates interior indoor shade.", "Partial Shade", "Low Water", "Well-Draining", "Small"),
        ("String of Pearls", "Senecio rowleyanus", 499, 8, "Trailing cascading vines with green pea-shaped succulent beads.", "Uniquely artistic hanging plant.", "Avoid overwatering, place in bright spot.", "Bright Indirect", "Low Water", "Gritty Mix", "Small"),
        ("Burro's Tail", "Sedum morganianum", 449, 10, "Plump blue-green trailing succulent tails.", "Charming hanging basket spec.", "Handle gently to prevent leaf drop.", "Bright Sunlight", "Low Water", "Perlite Sand", "Medium"),
        ("Crown of Thorns Pink", "Euphorbia milii", 379, 15, "Spiny woody stems with continuous bright pink flower bracts.", "Blooms non-stop in hot sun.", "Very drought hardy.", "Full Sun", "Very Low Water", "Dry Soil", "Medium"),
        ("Ghost Plant", "Graptopetalum paraguayense", 279, 25, "Pale pinkish gray powdery rosettes.", "Propagates effortlessly from fallen leaves.", "Full sun enhances pink hues.", "Full Sun", "Low Water", "Sandy Mix", "Small"),
        ("Panda Plant", "Kalanchoe tomentosa", 329, 18, "Fuzzy velvety silver leaves with dark chocolate edges.", "Fascinating soft touch succulent.", "Keep leaves dry while watering.", "Bright Sun", "Low Water", "Cactus Soil", "Small"),
        ("Christmas Cactus", "Schlumbergera bridgesii", 399, 12, "Arching flat segmented stems with vivid fuchsia flowers.", "Winter blooming houseplant.", "Keep away from harsh direct midday sun.", "Partial Shade", "Medium Water", "Peat Perlite", "Small"),
        ("Agave Americana", "Agave americana", 699, 6, "Dramatic blue-green rosette with sharp terminal spines.", "Bold desert landscape plant.", "Needs maximum sunshine and sharp drainage.", "Full Sun", "Negligible Water", "Rocky Sand", "Large"),
        ("Moon Cactus Red", "Gymnocalycium mihanovichii", 299, 20, "Bright ruby red grafted sphere on green cactus base.", "Colorful desktop novelty plant.", "Water lightly around the base.", "Filtered Light", "Low Water", "Standard Cactus", "Small"),
        ("Aeonium Black Rose", "Aeonium arboreum", 549, 10, "Deep burgundy purple rosette tree with dark fleshy leaves.", "Striking dark contrast plant.", "Goes dormant in summer heat.", "Full Sun", "Low Water", "Loamy Sand", "Medium"),
        ("Living Stones Lithops", "Lithops julii", 499, 5, "Fascinating succulents disguised as natural pebbles and stones.", "Extreme xeriscape curiosity.", "Water sparingly only twice a year.", "Direct Sun", "Minimal Water", "Pure Grit", "Small"),
        ("Bear's Paw", "Cotyledon tomentosa", 379, 12, "Fuzzy green leaves with red teeth resembling little bear paws.", "Adorable fuzzy texture.", "Protect from severe summer scorching.", "Bright Sunlight", "Low Water", "Sandy Potting", "Small"),
        ("Sedum Jelly Bean", "Sedum rubrotinctum", 249, 25, "Jellybean-like leaves that turn glossy red in sunshine.", "Colorful succulent accent.", "Easy propagation from cuttings.", "Full Sun", "Low Water", "Coarse Soil", "Small")
    ],
    "Air Purifying Plants": [
        ("Snake Plant Laurentii", "Sansevieria trifasciata 'Laurentii'", 549, 20, "Yellow-bordered sword leaves praised by NASA air research.", "Removes 107 known airborne toxins.", "Water monthly, impossible to kill.", "Low to Bright", "Low Water", "Cactus Loam", "Medium"),
        ("Peace Lily Supreme", "Spathiphyllum floribundum", 649, 15, "Lush broad leaves that actively eliminate ammonia and mold spores.", "Moistens dry air.", "Water when leaves droop slightly.", "Partial Shade", "Medium Water", "Organic Peat", "Medium"),
        ("Areca Palm Air Cleanser", "Dypsis lutescens", 949, 10, "Top rated natural air humidifier and toxin filter.", "Filters toluene and xylene.", "Water twice weekly.", "Bright Indirect", "Regular Water", "Loamy Mix", "Large"),
        ("Boston Fern Purifier", "Nephrolepis exaltata", 499, 18, "Removes indoor formaldehydes faster than almost any plant.", "Humidifies dry air-conditioned rooms.", "Mist regularly to keep fronds damp.", "Partial Shade", "High Water", "Peat Moss", "Medium"),
        ("Spider Plant Variegated", "Chlorophytum comosum 'Vittatum'", 319, 30, "Filters indoor carbon monoxide and cigarette smoke residues.", "Safe for curious pets.", "Water when top soil feels dry.", "Bright Light", "Moderate Water", "Potting Mix", "Small"),
        ("English Ivy", "Hedera helix", 429, 12, "Trailing vine that reduces airborne fecal particles and mold.", "Excellent for allergy sufferers.", "Keep soil cool and moist.", "Medium Light", "Regular Water", "Rich Soil", "Medium"),
        ("Aloe Vera Air Monitor", "Aloe barbadensis", 299, 25, "Leaves develop brown spots when air pollution levels rise.", "Cleans air while providing gel.", "Requires bright sunny windowsill.", "Full Light", "Low Water", "Sandy Mix", "Small"),
        ("Janet Craig Dracaena", "Dracaena deremensis", 749, 8, "Dark green tufted foliage that absorbs trichloroethylene.", "Ideal for newly painted office rooms.", "Wipe leaves clean occasionally.", "Low Light", "Moderate Water", "Standard Mix", "Large"),
        ("Rubber Tree Burgundy", "Ficus elastica 'Burgundy'", 799, 14, "Large glossy surface leaves trap airborne dust and spores.", "Filters airborne contaminants.", "Water when dry.", "Bright Light", "Medium Water", "Well Draining", "Large"),
        ("Bamboo Palm", "Chamaedorea seifrizii", 899, 10, "Elegant bamboo-like stems filtering benzene and trichloroethylene.", "Adds tropical serenity.", "Keep soil moist.", "Medium Light", "Regular Water", "Palm Mix", "Large"),
        ("Money Plant Golden", "Epipremnum aureum", 349, 40, "Tough golden vine that absorbs indoor electronic radiation VOCs.", "Brings luck and clean air.", "Grows in water or soil.", "Adaptable", "Medium Water", "Standard", "Small"),
        ("Weeping Fig Ficus", "Ficus benjamina", 849, 9, "Dense canopy filtering formaldehyde from furniture glues.", "Classic decor plant.", "Avoid moving pot frequently.", "Bright Sun", "Moderate Water", "Rich Soil", "Large"),
        ("Flamingo Flower Anthurium", "Anthurium andraeanum", 899, 10, "Absorbs household ammonia from cleaning chemicals.", "Stunning red flowers.", "Needs indirect warmth.", "Bright Indirect", "Regular Water", "Orchid Base", "Small"),
        ("Kimberly Queen Fern", "Nephrolepis obliterata", 529, 15, "Compact sword fern that cleans indoor pollutants cleanly.", "Less messy than Boston Fern.", "Keep soil damp.", "Partial Shade", "High Water", "Peat Mix", "Medium"),
        ("Broadleaf Lady Palm", "Rhapis excelsa", 1599, 5, "Multi-stemmed fan palm that removes indoor ammonia.", "Top choice for office foyers.", "Water deeply, shade lover.", "Shade", "Regular Water", "Rich Organic", "Large")
    ],
    "Ornamental Plants": [
        ("Calathea Orbifolia", "Goeppertia orbifolia", 899, 12, "Huge round silver-striped designer leaves.", "High fashion interior showpiece.", "Requires distilled water and high humidity.", "Filtered Shade", "High Water", "Peat Perlite", "Medium"),
        ("Coleus Rainbow", "Solenostemon scutellarioides", 249, 30, "Vibrant velvet foliage in neon magenta, yellow, and green.", "Instant color boost for pots.", "Pinch flowers to maintain foliage strength.", "Full Sun", "Daily Water", "Moist Soil", "Small"),
        ("Aglaonema Pink Anjamani", "Aglaonema hybrid", 699, 15, "Dazzling neon pink and green mottled leaves.", "Low light indoor designer favorite.", "Water when soil top dries out.", "Low Light", "Moderate Water", "Peat Mix", "Small"),
        ("Alocasia Polly African Mask", "Alocasia amazonica", 799, 10, "Dark arrow-shaped leathery leaves with bold white veins.", "Exotic sculptural plant.", "Keep warm, mist leaves frequently.", "Bright Indirect", "Medium Water", "Orchid Bark Mix", "Medium"),
        ("Philodendron Pink Princess", "Philodendron erubescens", 1499, 5, "Rare collector plant with splashy pink leaf variegation.", "High collector value.", "Provide climbing moss pole.", "Bright Indirect", "Moderate Water", "Chunk Mix", "Medium"),
        ("Stromanthe Triostar", "Stromanthe thalia", 749, 10, "Artistic leaf canvas of cream, green, and hot pink undersides.", "Dramatic prayer plant leaves.", "Keep humidity high.", "Partial Shade", "High Water", "Humus Rich", "Medium"),
        ("Croton Dust Star", "Codiaeum variegatum", 399, 20, "Deep green leaves speckled with golden starburst spots.", "Eye-catching pot accent.", "Bright sun keeps spots vivid.", "Full Sun", "Regular Water", "Garden Soil", "Medium"),
        ("Caladium Mixed", "Caladium hortulanum", 449, 18, "Paper-thin heart leaves in translucent red and white.", "Summer shade garden stunner.", "Dormant in winter season.", "Shade", "High Water", "Moist Peat", "Small"),
        ("Syngonium Pink Neon", "Syngonium podophyllum", 349, 25, "Arrowhead-shaped pastel pink leaves.", "Easy growing decorative climber.", "Trim stems to keep bushy.", "Indirect Sun", "Regular Water", "Potting Soil", "Small"),
        ("Cordyline Pink Diamond", "Cordyline fruticosa", 499, 15, "Upright palm-like leaves with vivid fuchsia margins.", "Tropical landscape accent.", "Water regularly in sunshine.", "Full Sun", "Regular Water", "Loamy Clay", "Large"),
        ("Maranta Red Prayer Plant", "Maranta leuconeura", 599, 12, "Herringbone red leaf veins that fold upward at night like hands.", "Fascinating daily leaf movements.", "Keep away from harsh sunlight.", "Shade", "High Water", "Peat Moss", "Small"),
        ("Fittonia Red Nerve", "Fittonia albivenis", 299, 30, "Delicate mosaic green leaves with bright crimson veins.", "Terrarium favorite.", "Faints when thirsty, revives instantly.", "Partial Shade", "High Water", "Moist Peat", "Small"),
        ("Rex Begonia", "Begonia rex-cultorum", 499, 15, "Swirled metallic silver and burgundy foliage.", "Intricate patterned leaves.", "Water soil without wetting leaves.", "Filtered Light", "Moderate Water", "Light Soil", "Small"),
        ("Tradescantia Zebrina", "Tradescantia zebrina", 279, 35, "Shimmering purple and silver striped trailing vine.", "Fast trailing basket filler.", "Bright light intensifies purple shade.", "Bright Light", "Regular Water", "Standard", "Small"),
        ("Alocasia Zebrina", "Alocasia zebrina", 1299, 6, "Distinctive leopard zebra-striped leaf stalks with arrow leaves.", "Architectural statement piece.", "Needs high humidity and space.", "Bright Indirect", "Medium Water", "Coarse Soil", "Large")
    ],
    "Fruit Plants": [
        ("Dwarf Mango Amrapali", "Mangifera indica", 899, 10, "Sweet dwarf mango tree suitable for large terrace containers.", "Yields delicious sweet mangoes.", "Needs full sunlight and seasonal fertilizer.", "Full Sun", "Regular Water", "Deep Loam", "Large"),
        ("Guava Thai Pink", "Psidium guajava", 499, 15, "Produces large crisp guavas with pink aromatic flesh.", "Rich in Vitamin C.", "Prune branches after fruiting.", "Full Sun", "Moderate Water", "Rich Garden", "Large"),
        ("Lemon Kagzi", "Citrus limon", 399, 25, "Thin-skinned juicy lemons produced all round the year.", "Abundant culinary citrus harvest.", "Feed with citrus fertilizer quarterly.", "Full Sun", "Regular Water", "Well-Draining", "Medium"),
        ("Pomegranate Bhagwa", "Punica granatum", 599, 12, "Deep red arils bursting with sweet antioxidant juice.", "Hardy drought tolerant fruit tree.", "Water deeply during fruit development.", "Full Sun", "Low Water", "Clay Loam", "Medium"),
        ("Papaya Red Lady", "Carica papaya", 299, 30, "Fast-growing dwarf papaya bearing sweet orange fruits.", "Fruits within 8 to 10 months.", "Requires sunny spot with great drainage.", "Full Sun", "Daily Water", "Organic Rich", "Large"),
        ("Chiku Sapota", "Manilkara zapota", 549, 12, "Sweet brown sapodilla fruit with malty caramel flavor.", "Long-lived sturdy fruit tree.", "Water moderately once established.", "Full Sun", "Moderate Water", "Deep Soil", "Large"),
        ("Fig Anjeer", "Ficus carica", 649, 10, "Sweet succulent figs harvested twice a year.", "High fiber nutritious fruit.", "Tolerates container pot growth well.", "Full Sun", "Moderate Water", "Sandy Loam", "Medium"),
        ("Sweet Lime Mosambi", "Citrus sinensis", 699, 8, "Refreshing sweet citrus juice fruit tree.", "Hydrating fresh fruit.", "Protect from severe waterlogging.", "Full Sun", "Regular Water", "Loamy Mix", "Large"),
        ("Star Fruit Carambola", "Averrhoa carambola", 749, 7, "Juicy star-shaped crunchy fruits produced abundantly.", "Exotic decorative fresh fruit.", "Keep soil evenly moist.", "Full Sun", "Regular Water", "Rich Loam", "Large"),
        ("Custard Apple Sitaphal", "Annona squamosa", 499, 14, "Creamy sweet custard fruit with rich aromatic pulp.", "Delicious dessert fruit.", "Water moderately, dry climate lover.", "Full Sun", "Low Water", "Dry Soil", "Medium"),
        ("Mulberry Black", "Morus nigra", 399, 20, "Sweet dark berries harvested directly from fast-growing bush.", "Superfood berry rich in antioxidants.", "Easy to grow and prune.", "Full Sun", "Regular Water", "Garden Soil", "Medium"),
        ("Dragon Fruit Red", "Hylocereus costaricensis", 599, 15, "Vibrant pink climbing cactus bearing magenta pitaya fruit.", "Exotic high value fruit.", "Requires sturdy climbing post.", "Full Sun", "Low Water", "Sandy Cactus", "Large"),
        ("Passion Fruit Purple", "Passiflora edulis", 449, 18, "Vigorous vine with intricate flowers and aromatic tangy fruit.", "Delicious juice flavor.", "Provide fence or arbor trellis.", "Full Sun", "High Water", "Rich Compost", "Large"),
        ("Barbados Cherry", "Malpighia emargina", 499, 12, "Bright red tart cherries containing massive Vitamin C.", "High vitamin superfruit.", "Bushy growth easy for containers.", "Full Sun", "Regular Water", "Loam Soil", "Medium"),
        ("Dwarf Orange Kinnu", "Citrus reticulata", 799, 9, "Juicy sweet orange mandarin oranges on compact trees.", "Festive citrus harvest.", "Needs direct sun exposure.", "Full Sun", "Regular Water", "Rich Mix", "Medium")
    ],
    "Vegetable Plants": [
        ("Tomato Cherry Red", "Solanum lycopersicum", 149, 40, "High yielding cherry tomatoes bursting with sweet flavor.", "Easy container vegetable harvest.", "Stake plant, water at root base.", "Full Sun", "Daily Water", "Rich Loam", "Medium"),
        ("Chilli Hybrid Red", "Capsicum annuum", 129, 50, "Pungent spicy green and red hot peppers for kitchen cooking.", "Abundant spicy pepper yield.", "Sunny spot, avoid wet leaves.", "Full Sun", "Regular Water", "Garden Soil", "Small"),
        ("Brinjal Eggplant Purple", "Solanum melongena", 139, 35, "Glossy deep purple oval aubergines.", "Staple cooking vegetable.", "Feed with organic compost monthly.", "Full Sun", "Daily Water", "Nutrient Soil", "Medium"),
        ("Lady Finger Okra", "Abelmoschus esculentus", 119, 45, "Crisp tender green okra pods.", "Fast growing summer crop.", "Harvest pods while young and tender.", "Full Sun", "Daily Water", "Warm Loam", "Medium"),
        ("Spinach Palak", "Spinacia oleracea", 99, 60, "Nutritious leafy green spinach rich in iron.", "Harvest continuous leaves.", "Keep soil moist in shade or sun.", "Partial Sun", "High Water", "Organic Compost", "Small"),
        ("Capsicum Bell Pepper", "Capsicum annuum var. grossum", 159, 30, "Crisp sweet green bell peppers.", "Perfect for salads and stir fries.", "Provide stem support for heavy peppers.", "Full Sun", "Regular Water", "Rich Loam", "Small"),
        ("Cucumber Green", "Cucumis sativus", 129, 40, "Cool hydrating cucumbers produced on scrambling vines.", "Fresh crisp salad vegetable.", "Trellis climbing support recommended.", "Full Sun", "Daily Water", "Moist Soil", "Medium"),
        ("Bitter Gourd Karela", "Momordica charantia", 139, 25, "Traditional medicinal bitter gourd climber.", "Helps maintain healthy blood sugar.", "Provide trellis support.", "Full Sun", "Regular Water", "Garden Loam", "Large"),
        ("Bottle Gourd Lauki", "Lagenaria siceraria", 149, 20, "Smooth long green gourds on fast growing vines.", "Cooling digestive vegetable.", "Loves sunny open terrace space.", "Full Sun", "Daily Water", "Deep Loam", "Large"),
        ("Radish White Mooli", "Raphanus sativus", 99, 50, "Crisp white peppery root radishes.", "Ready to harvest in just 30 days.", "Keep soil soft and uncompacted.", "Full Sun", "Regular Water", "Sandy Soft", "Small"),
        ("Cabbage Green", "Brassica oleracea var. capitata", 139, 30, "Dense round heads of crisp green cabbage.", "Rich in Vitamin K and fiber.", "Protect heads from caterpillars.", "Full Sun", "Regular Water", "Moist Clay", "Medium"),
        ("Cauliflower White", "Brassica oleracea var. botrytis", 149, 25, "Tender white curd head surrounded by green leaves.", "Delicious fresh vegetable.", "Water soil, avoid soaking curds.", "Full Sun", "Regular Water", "Rich Compost", "Medium"),
        ("Coriander Vegetable", "Coriandrum sativum", 89, 70, "Fresh aromatic coriander greens.", "Essential kitchen culinary herb.", "Sow seeds shallowly.", "Partial Sun", "Daily Water", "Standard", "Small"),
        ("Mint Pudina Veg", "Mentha spicata", 119, 50, "Fast spreading fresh mint shoots for kitchen recipes.", "Continuous green harvest.", "Water daily in warm weather.", "Partial Shade", "High Water", "Wet Soil", "Small"),
        ("Curry Leaves Sapling", "Murraya koenigii", 249, 20, "Essential aromatic leaf plant for fresh kitchen cooking.", "Adds rich aroma to dishes.", "Prune tips for lush growth.", "Full Sun", "Regular Water", "Organic Loam", "Medium")
    ],
    "Cactus Plants": [
        ("Golden Barrel Cactus", "Echinocactus grusonii", 599, 10, "Symmetrical globe-shaped cactus with bright golden yellow spines.", "Striking geometric desert plant.", "Needs intense sunshine and minimal water.", "Full Sun", "Negligible Water", "Gritty Sand", "Medium"),
        ("Bunny Ears Cactus", "Opuntia microdasys", 349, 20, "Polka-dot yellow pads shaped like rabbit ears.", "Charming decorative cactus.", "Avoid touching yellow glochids.", "Full Sun", "Very Low Water", "Coarse Soil", "Small"),
        ("Old Man Cactus", "Cephalocereus senilis", 499, 8, "Tall columnar cactus covered in long shaggy white hair.", "Unusual hairy cactus species.", "Protect hair from dirt and excessive wetness.", "Full Sun", "Low Water", "Sandy Grit", "Medium"),
        ("Saguaro Mini Cactus", "Carnegiea gigantea", 799, 5, "Classic iconic Arizona desert branching cactus.", "Architectural cactus icon.", "Extremely drought hardy.", "Full Sun", "Minimal Water", "Rocky Sand", "Large"),
        ("Bishop's Cap Cactus", "Astrophytum myriostigma", 449, 12, "Spineless star-shaped cactus covered in white flecks.", "Smooth tactile cactus.", "Prefers warm dry air.", "Bright Sun", "Low Water", "Porous Soil", "Small"),
        ("Rebutia Orange Flower", "Rebutia minuscula", 299, 25, "Cluster cactus producing vivid orange flowers in spring.", "Prolific blooming cactus.", "Keep dry during winter rest.", "Full Sun", "Low Water", "Standard Cactus", "Small"),
        ("Organ Pipe Cactus", "Stenocereus thurberi", 649, 7, "Multi-stemmed upright cactus resembling organ pipes.", "Dramatic vertical lines.", "Full direct sunlight lover.", "Full Sun", "Very Low Water", "Dry Soil", "Large"),
        ("Feather Cactus", "Mammillaria plumosa", 399, 15, "Soft ball cactus covered in downy feather-like white spines.", "Fuzzy soft appearance.", "Water strictly from the bottom.", "Bright Light", "Low Water", "Perlite Grit", "Small"),
        ("Blue Myrtle Cactus", "Myrtillocactus geometrizans", 499, 10, "Smooth glaucous blue-green branched columnar cactus.", "Sleek modern aesthetics.", "Fast growing columnar species.", "Full Sun", "Low Water", "Well Draining", "Medium"),
        ("Pincushion Cactus", "Mammillaria crinita", 279, 30, "Small globose cactus topped with ring of pink flowers.", "Great for window sill displays.", "Water lightly in summer.", "Full Sun", "Low Water", "Sandy Potting", "Small"),
        ("Rat Tail Cactus", "Aporocactus flagelliformis", 449, 12, "Long whip-like drooping stems bearing tubular red flowers.", "Spectacular hanging pot cactus.", "Give bright filtered sun.", "Bright Indirect", "Low Water", "Cactus Mix", "Medium"),
        ("Horse Crippler Cactus", "Echinocactus texensis", 549, 8, "Flattish rigid cactus with heavy curved pinkish spines.", "Rugged tough cactus specimen.", "Resists extreme cold and heat.", "Full Sun", "Negligible Water", "Hard Clay Sand", "Medium"),
        ("Mammillaria Elongata", "Mammillaria elongata", 319, 20, "Golden star cluster cactus with tightly packed slender stems.", "Forms dense golden mats.", "Easy for beginner cactus growers.", "Full Sun", "Low Water", "Porous Grit", "Small"),
        ("Gymnocalycium Chin", "Gymnocalycium baldianum", 349, 18, "Ribbed round cactus blooming in deep crimson red.", "Frequent floral display.", "Keep dry in winter.", "Full Sun", "Low Water", "Gritty Mix", "Small"),
        ("Opuntia Prickly Pear", "Opuntia ficus-indica", 399, 15, "Flat green paddle cactus bearing edible prickly pear fruits.", "Traditional desert fruit cactus.", "Plant in sunny spacious spot.", "Full Sun", "Very Low Water", "Dry Sand", "Large")
    ],
    "Bonsai Plants": [
        ("Ficus Retusa Bonsai", "Ficus retusa", 1499, 10, "Classic curved ginseng root trunk with dark glossy canopy.", "Symbol of peace and balance.", "Water when soil top dries out, mist leaves.", "Bright Indirect", "Moderate Water", "Bonsai Loam", "Medium"),
        ("Japanese Red Maple Bonsai", "Acer palmatum", 2999, 4, "Breathtaking miniature maple with fiery crimson autumn leaves.", "Exotic luxury landscape artwork.", "Protect from scorching afternoon sun.", "Filtered Sun", "Regular Water", "Acidic Bonsai", "Medium"),
        ("Juniper Procumbens Bonsai", "Juniperus procumbens", 1899, 8, "Traditional needle evergreen styled in cascading wind-swept form.", "Iconic evergreen bonsai.", "Keep outdoors in full sunlight.", "Full Sun", "Moderate Water", "Gritty Grit", "Medium"),
        ("Chinese Elm Bonsai", "Ulmus parvifolia", 1299, 12, "Small intricate serrated leaves on gracefully twisted woody trunk.", "Very forgiving for beginners.", "Prune back shoots to 2 leaves.", "Partial Sun", "Regular Water", "Bonsai Mix", "Medium"),
        ("Carmona Fukien Tea Bonsai", "Carmona microphylla", 1399, 10, "Glossy dark green leaves with delicate white star flowers and red berries.", "Blooms indoors periodically.", "Keep moist and warm.", "Bright Indirect", "Regular Water", "Organic Loam", "Small"),
        ("Jade Tree Bonsai", "Crassula ovata bonsai", 999, 15, "Thick succulent trunk with miniature shiny rounded leaves.", "Resilient low water bonsai.", "Water sparingly, sunny position.", "Full Sun", "Low Water", "Coarse Sand", "Small"),
        ("Schefflera Umbrella Bonsai", "Schefflera arboricola", 1199, 12, "Miniature palmately compound leaf canopy with aerial prop roots.", "Thrives in indoor humidity.", "Water when top soil feels dry.", "Bright Light", "Medium Water", "Standard Mix", "Medium"),
        ("Podocarpus Buddhist Pine", "Podocarpus costalis", 1599, 7, "Elegant dark evergreen needle leaves on formal upright trunk.", "Symbol of wisdom and dignity.", "Keep soil evenly moist.", "Partial Sun", "Regular Water", "Peat Grit", "Medium"),
        ("Bougainvillea Bonsai", "Bougainvillea hybrid bonsai", 1799, 6, "Gnarled woody trunk bursts with electric pink floral bracts.", "Stunning flowering bonsai.", "Full sunshine required for blooms.", "Full Sun", "Moderate Water", "Clay Mix", "Medium"),
        ("Azalea Satsuki Bonsai", "Rhododendron indica", 2499, 5, "Miniature shrub styled into dense floral clouds of pink and white.", "Japanese exhibition flower bonsai.", "Requires acidic moist substrate.", "Partial Sun", "High Water", "Kanuma Soil", "Small"),
        ("Banyan Tree Ficus Bonsai", "Ficus benghalensis", 1699, 8, "Sprawling aerial roots forming majestic miniature sacred tree.", "Sacred Indian banyan look.", "High humidity and warm temp.", "Bright Sun", "Regular Water", "Rich Soil", "Large"),
        ("Olive Tree Bonsai", "Olea europaea", 2299, 5, "Silvery slender leaves on ancient weathered twisting grey trunk.", "Symbol of peace and victory.", "Full direct sunshine lover.", "Full Sun", "Low Water", "Calcareous Grit", "Medium"),
        ("Wisteria Purple Bonsai", "Wisteria sinensis", 2799, 4, "Cascading long clusters of fragrant violet flowers in early spring.", "Dramatic floral waterfall.", "Requires moist soil during bloom.", "Full Sun", "High Water", "Nutrient Mix", "Large"),
        ("Cedar Atlas Bonsai", "Cedrus atlantica", 2199, 5, "Bluish needle clusters on formal upright weathered evergreen trunk.", "Stately conifer bonsai.", "Outdoors year round.", "Full Sun", "Moderate Water", "Sharp Grit", "Large"),
        ("Black Pine Japanese Bonsai", "Pinus thunbergii", 3499, 3, "Master-level evergreen bonsai with dark rigid needle pairs.", "King of Japanese bonsai.", "Requires needle pinching skills.", "Full Sun", "Moderate Water", "Akadama Kiryu", "Large")
    ]
}

SERVICES_DATA = [
    {"name": "Plant Care Consultation", "price": 499, "description": "1-on-1 expert diagnosis of plant health, soil conditions, pest management, and custom care schedules.", "image": "images/services/consultation.jpg"},
    {"name": "Home Plant Maintenance", "price": 999, "description": "Bi-weekly or monthly professional garden and indoor plant cleaning, pruning, fertilizing, and watering service.", "image": "images/services/maintenance.jpg"},
    {"name": "Plant Repotting Service", "price": 349, "description": "Professional repotting into fresh nutrient-rich soil mix with larger aesthetic pots.", "image": "images/services/repotting.jpg"},
    {"name": "Plant Delivery & Setup", "price": 299, "description": "Safe white-glove transport and perfect placement of large plants at your home or balcony.", "image": "images/services/delivery.jpg"},
    {"name": "Garden Setup & Design", "price": 2499, "description": "Complete terrace, backyard, or balcony garden design, planter installation, and layout transformation.", "image": "images/services/garden.jpg"},
    {"name": "Indoor Plant Setup", "price": 1499, "description": "Curated interior styling with air-purifying plants tailored to your living room lighting.", "image": "images/services/indoor.jpg"},
    {"name": "Office Plant Setup", "price": 3499, "description": "Commercial green office installation designed to boost employee productivity and air quality.", "image": "images/services/office.jpg"},
    {"name": "Plant Health Consultation", "price": 599, "description": "Emergency site visit for ailing plants with organic pest treatments and root resuscitation.", "image": "images/services/health.jpg"}
]

def generate_svg_image_if_missing(filepath, title, category_name):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not os.path.exists(filepath):
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1b4332"/>
      <stop offset="50%" stop-color="#2d6a4f"/>
      <stop offset="100%" stop-color="#52b788"/>
    </linearGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="#000" flood-opacity="0.3"/>
    </filter>
  </defs>
  <rect width="400" height="400" fill="url(#bg)"/>
  <circle cx="200" cy="180" r="110" fill="#ffffff" opacity="0.15"/>
  <g filter="url(#shadow)" transform="translate(140, 100)">
    <path d="M60 160 C 60 160, 20 100, 20 60 C 20 20, 60 0, 60 0 C 60 0, 100 20, 100 60 C 100 100, 60 160, 60 160 Z" fill="#d8f3dc"/>
    <path d="M60 160 C 60 160, 30 110, 45 70 C 55 40, 60 10, 60 10 C 60 10, 75 40, 75 70 C 90 110, 60 160, 60 160 Z" fill="#b7e4c7"/>
    <path d="M60 160 L 60 10" stroke="#1b4332" stroke-width="3" stroke-linecap="round"/>
    <ellipse cx="60" cy="165" rx="35" ry="12" fill="#74c69d"/>
    <path d="M35 165 L 45 190 L 75 190 L 85 165 Z" fill="#40916c"/>
  </g>
  <rect x="20" y="310" width="360" height="70" rx="10" fill="#ffffff" opacity="0.9"/>
  <text x="200" y="340" font-family="'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="bold" fill="#1b4332" text-anchor="middle">{title}</text>
  <text x="200" y="365" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="600" fill="#52b788" text-anchor="middle">{category_name.upper()} • GREENCART</text>
</svg>'''
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)

def seed_database():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")

        # 1. Seed Demo Users
        admin = User.query.filter_by(email='admin@greencart.com').first()
        if not admin:
            admin = User(
                name="GreenCart Administrator",
                email="admin@greencart.com",
                phone="9876543210",
                username="admin",
                role="ADMIN",
                status="ACTIVE"
            )
            admin.set_password("admin123")
            db.session.add(admin)
            print("Created Admin Account: admin / admin123")

        customer1 = User.query.filter_by(email="john@example.com").first()
        if not customer1:
            customer1 = User(
                name="John Doe",
                email="john@example.com",
                phone="9876543211",
                username="customer1",
                role="CUSTOMER",
                status="ACTIVE"
            )
            customer1.set_password("cust123")
            db.session.add(customer1)
            db.session.flush()

            # Address & Cart
            addr1 = Address(user_id=customer1.id, address="123 Green Avenue, Flat 4B", city="Mumbai", state="Maharashtra", pincode="400001", is_default=True)
            cart1 = Cart(user_id=customer1.id)
            db.session.add_all([addr1, cart1])
            print("Created Demo Customer 1: customer1 / cust123")

        dp1 = User.query.filter_by(email="alex@greencart.com").first()
        if not dp1:
            dp1 = User(
                name="Alex Swift (Delivery Partner)",
                email="alex@greencart.com",
                phone="9876543212",
                username="delivery1",
                role="DELIVERY_PARTNER",
                status="ACTIVE"
            )
            dp1.set_password("del123")
            db.session.add(dp1)
            db.session.flush()

            dp_prof = DeliveryPartner(user_id=dp1.id, availability_status="Available", current_status="Ready for orders", vehicle_type="Two Wheeler")
            db.session.add(dp_prof)
            print("Created Demo Delivery Partner 1: delivery1 / del123")

        db.session.commit()

        # 2. Seed Categories
        category_map = {}
        for cat_info in CATEGORIES_DATA:
            cat_img_relative = f"images/categories/{cat_info['slug']}.jpg"
            cat = Category.query.filter_by(name=cat_info['name']).first()
            if not cat:
                cat = Category(
                    name=cat_info['name'],
                    slug=cat_info['slug'],
                    description=cat_info['description'],
                    image=cat_img_relative
                )
                db.session.add(cat)
                db.session.flush()
            else:
                cat.image = cat_img_relative
                
            category_map[cat_info['name']] = cat

        db.session.commit()
        print("Seeded 12 Category Cover Images.")

        # 3. Seed 180 Plants (15 per category)
        plant_count = 0
        all_seeded_plants = []
        plants_dir = os.path.join(app.root_path, 'static', 'images', 'plants')
        all_custom_images = [f for f in os.listdir(plants_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))] if os.path.exists(plants_dir) else []
        
        PLANT_IMAGE_ALIASES = {
            "devil's ivy pothos": "1788814772_11.jpg",
            "chrysanthemum yellow": "1788808195_yellow.jpg",
            "stevia sugar plant": "1788813262_Stevia_Medicinal.jpg",
            "crown of thorns pink": "1788809848_Rebutia_Orange_Flower.jpg",
            "blue myrtle cactus": "1788809647_Myrtillocactus_geometrizans.jpg",
            "podocarpus buddhist pine": "1788808254_Black_Pine_Japanese_Bonsai.jpg",
            "bougainvillea bonsai": "1788808344_Wisteria_Purple_Bonsai.jpg",
            "cedar atlas bonsai": "1788808312_cedr_atlas_bonasi.jpg"
        }
        
        for cat_name, plants_list in PLANTS_BY_CATEGORY.items():
            cat_obj = category_map[cat_name]
            cat_folder_slug = cat_obj.slug
            
            for p_info in plants_list:
                name, sci_name, price, stock, desc, benefits, care, sun, water, soil, size = p_info
                name_lower = name.lower()
                plant_slug = name_lower.replace(' ', '_').replace("'", '').replace('-', '_')
                
                # Default SVG fallback
                relative_img_path = f"images/plants/{cat_folder_slug}/{plant_slug}.svg"
                full_img_path = os.path.join(app.root_path, 'static', relative_img_path)
                generate_svg_image_if_missing(full_img_path, name, cat_name)
                
                # Check for real custom uploaded JPG/PNG image for this plant
                matched_jpg = None
                if name_lower in PLANT_IMAGE_ALIASES:
                    matched_jpg = f"images/plants/{PLANT_IMAGE_ALIASES[name_lower]}"
                else:
                    clean_name_parts = [p for p in plant_slug.split('_') if len(p) > 2]
                    for custom_img in all_custom_images:
                        c_lower = custom_img.lower().replace('-', '_')
                        if plant_slug in c_lower or (len(clean_name_parts) >= 2 and all(part in c_lower for part in clean_name_parts[:2])):
                            matched_jpg = f"images/plants/{custom_img}"
                            break
                        
                final_image_path = matched_jpg if matched_jpg else relative_img_path
                
                existing_plant = Plant.query.filter_by(name=name, category_id=cat_obj.id).first()
                if existing_plant:
                    existing_plant.image = final_image_path
                    if existing_plant.stock_quantity != stock:
                        existing_plant.stock_quantity = stock
                else:
                    discount = 10.0 if plant_count % 3 == 0 else 0.0
                    rating = round(4.0 + (plant_count % 10) * 0.1, 1)
                    
                    new_p = Plant(
                        category_id=cat_obj.id,
                        name=name,
                        scientific_name=sci_name,
                        description=desc,
                        benefits=benefits,
                        care_instructions=care,
                        sunlight=sun,
                        water_requirement=water,
                        soil_type=soil,
                        size=size,
                        price=price,
                        discount=discount,
                        stock_quantity=stock,
                        image=final_image_path,
                        status='ACTIVE' if stock > 0 else 'OUT_OF_STOCK',
                        rating=rating,
                        reviews_count=(plant_count % 15) + 3
                    )
                    db.session.add(new_p)
                    all_seeded_plants.append(new_p)
                    plant_count += 1

        db.session.commit()
        print(f"Seeded {plant_count} Plants across 12 Categories!")

        # 4. Seed Services
        for s_info in SERVICES_DATA:
            serv = Service.query.filter_by(name=s_info['name']).first()
            if not serv:
                serv = Service(
                    name=s_info['name'],
                    description=s_info['description'],
                    price=s_info['price'],
                    image=s_info['image'],
                    status='ACTIVE'
                )
                db.session.add(serv)
            else:
                serv.image = s_info['image']

        db.session.commit()
        print("Seeded 8 Plant Service Cover Images.")

        # 5. Seed Initial Sample Orders for Demonstration & Admin Analytics
        if Order.query.count() == 0 and customer1:
            sample_p1 = Plant.query.filter_by(name="Snake Plant").first()
            sample_p2 = Plant.query.filter_by(name="Peace Lily").first()
            
            if sample_p1 and sample_p2:
                # Order 1: Delivered
                o1 = Order(
                    user_id=customer1.id,
                    total_amount=1098.0,
                    delivery_fee=0.0,
                    tax_amount=54.9,
                    grand_total=1152.9,
                    payment_status='Successful',
                    order_status='Delivered',
                    delivery_partner_id=dp1.id,
                    delivery_address="John Doe, 9876543211\n123 Green Avenue, Flat 4B, Mumbai - 400001",
                    created_at=datetime.utcnow() - timedelta(days=2)
                )
                db.session.add(o1)
                db.session.flush()
                
                oi1 = OrderItem(order_id=o1.id, plant_id=sample_p1.id, quantity=1, price=sample_p1.final_price, plant_name=sample_p1.name, plant_image=sample_p1.image)
                oi2 = OrderItem(order_id=o1.id, plant_id=sample_p2.id, quantity=1, price=sample_p2.final_price, plant_name=sample_p2.name, plant_image=sample_p2.image)
                pay1 = Payment(order_id=o1.id, user_id=customer1.id, amount=o1.grand_total, payment_method='UPI', transaction_id='TXN-DEMO1001', payment_status='Successful', payment_date=o1.created_at)
                db.session.add_all([oi1, oi2, pay1])
                
                # Order 2: Active / Out for Delivery
                o2 = Order(
                    user_id=customer1.id,
                    total_amount=499.0,
                    delivery_fee=49.0,
                    tax_amount=24.95,
                    grand_total=572.95,
                    payment_status='Successful',
                    order_status='Out for Delivery',
                    delivery_partner_id=dp1.id,
                    delivery_address="John Doe, 9876543211\n123 Green Avenue, Flat 4B, Mumbai - 400001",
                    created_at=datetime.utcnow() - timedelta(hours=3)
                )
                db.session.add(o2)
                db.session.flush()
                
                oi3 = OrderItem(order_id=o2.id, plant_id=sample_p1.id, quantity=1, price=sample_p1.final_price, plant_name=sample_p1.name, plant_image=sample_p1.image)
                pay2 = Payment(order_id=o2.id, user_id=customer1.id, amount=o2.grand_total, payment_method='Credit/Debit Card', transaction_id='TXN-DEMO1002', payment_status='Successful', payment_date=o2.created_at)
                db.session.add_all([oi3, pay2])
                
                db.session.commit()
                print("Seeded Demo Orders & Payments for Admin Dashboard graphs.")

        print("\nGreenCart Database Initialization & Seeding Complete!")

if __name__ == '__main__':
    seed_database()
