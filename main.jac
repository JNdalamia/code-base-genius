import from byllm.llm { Model }
import from dotenv { load_dotenv }
import os;
include utils;
import from utils { clone_repo }
import from utils { file_tree_generator }
import from utils { analyze_repo_structure }



glob llm = Model(model_name="gemini/gemini-2.0-flash");


enum YesNo { 
    YES = "Yes", 
    NO = "No" 
}

# node Repo{
#     has repo_url: str;
#     has name: str;
# }


walker code_genius{
    has github_url : str;

    obj __specs__ {
        static has auth: bool = False;
    }

    '''Verify if a GitHub repository is valid and public.'''
    def verify_repo(url: str) -> YesNo by llm();

    can start with `root entry;

}

walker repo_mapper{
    has repo_url: str;
    has repo_name: str;



    '''Delegate cloning to the external tool and return the resulting local path.'''
    def agentic_clone(url: str, name: str) -> str by llm(
        tools=[clone_repo] 
    ); 

    def build_tree_structure(repo_dir: str) -> str by llm(
        tools=[ file_tree_generator]
    );
    '''
    Looks for a standard README file and return its summary.
    If no README is found, create summary of 3-5 sentence of repo  .
    '''   
    def summairize_repo(repo_url : str) -> str by llm();

  
    can start with `root entry;

}

walker code_analyzer{

    has repo_dir: str;
    has tree_structure: str;
    has summary: str;
    has repo_name: str;
    has repo_url: str;

    '''
    Analyzes the structure of files in a repository based on a 
    JSON string representation of the file tree.
    '''
    def analyze_repo(repo_dir: str, tree_structure: str) -> str by llm(
        tools=[analyze_repo_structure]
    );


    can start with `root entry;


}


walker doc_genie{

    has data: dict[str, str];

    '''
    Convert data given into a well‑organised markdown document. Include sections for project overview, 
    installation, usage, and API reference. Ensure the markdown is clear, logically ordered and human‑readable. Use 
    headings, bullet points, tables and diagrams judiciously.
    '''
    def generate_doc(data: dict[str, str]) -> str by llm();

    
    can start with `root entry;

}

with entry{
    load_dotenv();

}