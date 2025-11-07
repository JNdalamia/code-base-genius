impl code_genius.start{

    github_url = self.github_url;
    verification = self.verify_repo(github_url);
    if verification == YesNo.YES {
        repo_name = github_url.split("/")[-1].replace(".git", "");

        mapper_walker = root spawn repo_mapper(repo_url=github_url, repo_name=repo_name); 
        # if(mapper_walker) {
        #      report {
        #     "status": "success",
        #     "message": f"Repository '{repo_name}' is being cloned.",
        #     "repo_name": repo_name,
        #     "repo_url": github_url,
        # };
        # }
       
    } else {
        report(f"Repository {github_url} verification failed.");
    }

}

impl repo_mapper.start{
    print("Mapping repository structure..."); 
    
    repo_dir = self.agentic_clone(self.repo_url, self.repo_name);
    tree_structure = self.build_tree_structure(repo_dir);
    summary = self.summairize_repo(self.repo_url);
    
    code_analyzer_walker = root spawn code_analyzer(
        repo_dir=repo_dir,
        tree_structure=str(tree_structure),
        summary=summary,
        repo_name=self.repo_name,
        repo_url=self.repo_url
    );

}


impl code_analyzer.start{
    print("Analyzing code...");

    analysis_report = self.analyze_repo(self.repo_url, self.tree_structure);

    data = {
            "repo_dir": self.repo_dir,
            "analysis_report": analysis_report,
            "summary": self.summary,
            "repo_name": self.repo_name,
            "repo_url": self.repo_url,
            "tree_structure": self.tree_structure
    };

    doc_genie_walker = root spawn doc_genie(data=data);

}

impl doc_genie.start{
    print("Generating documentation...");


    markdown_file = self.generate_doc(self.data);

    report {
        "status": "success",
        "repo_name": self.data["repo_name"],
        "markdown_file": markdown_file
    };

}