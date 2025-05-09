from chunker_pipeline import chunker, SentenceTransformerEmbeddings
from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings
from vectordb_pipeline import *;


client = connect_to_client()

# Creating Collection
# create_collection(client, "tutorlm_main")
# close_client(client)

# Opening Main Collection
collec = get_collection(client, 'tutorlm_main')


text = """Photosynthesis (/ˌfoʊtəˈsɪnθəsɪs/ FOH-tə-SINTH-ə-sis)[1] is a system of biological processes by which photosynthetic organisms, such as most plants, algae, and cyanobacteria, convert light energy, typically from sunlight, into the chemical energy necessary to fuel their metabolism. Photosynthesis usually refers to oxygenic photosynthesis, a process that produces oxygen. Photosynthetic organisms store the chemical energy so produced within intracellular organic compounds (compounds containing carbon) like sugars, glycogen, cellulose and starches. To use this stored chemical energy, an organism's cells metabolize the organic compounds through cellular respiration. Photosynthesis plays a critical role in producing and maintaining the oxygen content of the Earth's atmosphere, and it supplies most of the biological energy necessary for complex life on Earth.[2]

Some bacteria also perform anoxygenic photosynthesis, which uses bacteriochlorophyll to split hydrogen sulfide as a reductant instead of water, producing sulfur instead of oxygen. Archaea such as Halobacterium also perform a type of non-carbon-fixing anoxygenic photosynthesis, where the simpler photopigment retinal and its microbial rhodopsin derivatives are used to absorb green light and power proton pumps to directly synthesize adenosine triphosphate (ATP), the "energy currency" of cells. Such archaeal photosynthesis might have been the earliest form of photosynthesis that evolved on Earth, as far back as the Paleoarchean, preceding that of cyanobacteria (see Purple Earth hypothesis).

While the details may differ between species, the process always begins when light energy is absorbed by the reaction centers, proteins that contain photosynthetic pigments or chromophores. In plants, these pigments are chlorophylls (a porphyrin derivative that absorbs the red and blue spectrums of light, thus reflecting green) held inside chloroplasts, abundant in leaf cells. In bacteria, they are embedded in the plasma membrane. In these light-dependent reactions, some energy is used to strip electrons from suitable substances, such as water, producing oxygen gas. The hydrogen freed by the splitting of water is used in the creation of two important molecules that participate in energetic processes: reduced nicotinamide adenine dinucleotide phosphate (NADPH) and ATP.

In plants, algae, and cyanobacteria, sugars are synthesized by a subsequent sequence of light-independent reactions called the Calvin cycle. In this process, atmospheric carbon dioxide is incorporated into already existing organic compounds, such as ribulose bisphosphate (RuBP).[3] Using the ATP and NADPH produced by the light-dependent reactions, the resulting compounds are then reduced and removed to form further carbohydrates, such as glucose. In other bacteria, different mechanisms like the reverse Krebs cycle are used to achieve the same end.

The first photosynthetic organisms probably evolved early in the evolutionary history of life using reducing agents such as hydrogen or hydrogen sulfide, rather than water, as sources of electrons.[4] Cyanobacteria appeared later; the excess oxygen they produced contributed directly to the oxygenation of the Earth,[5] which rendered the evolution of complex life possible. The average rate of energy captured by global photosynthesis is approximately 130 terawatts,[6][7][8] which is about eight times the total power consumption of human civilization.[9] Photosynthetic organisms also convert around 100–115 billion tons (91–104 Pg petagrams, or billions of metric tons), of carbon into biomass per year.[10][11] Photosynthesis was discovered in 1779 by Jan Ingenhousz who showed that plants need light, not just soil and water."""

# c_chunker = chunker(SentenceTransformerEmbeddings(SentenceTransformer('Snowflake/snowflake-arctic-embed-l-v2.0')))

# chunks = [{'data': c} for c in c_chunker.chunk([text])]
# print(chunks)
# add_data(collec, chunks, ['data'])
print_data(query_data(collec, 'photosynthesis', 2))

close_client(client)