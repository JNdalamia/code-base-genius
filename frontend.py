# streamlit_app.py

import streamlit as st
import requests

st.set_page_config(page_title="Codebase Genius", layout="wide")

st.title("🧠 Codebase Genius: GitHub Repo Analyzer & Doc Generator")

# Input Section
st.sidebar.header("🔗 Repository Input")
github_url = st.sidebar.text_input("Enter GitHub Repository URL", placeholder="https://github.com/user/repo")

if github_url:
    st.sidebar.success("URL received. Ready to process.")

    # Step 1: Verify Repository
    if st.button("✅ Verify Repository"):
        with st.spinner("Verifying repository..."):
            response = requests.post("http://localhost:8000/verify_repo", json={"url": github_url})
            st.write("Verification Result:", response.json().get("result", "No response"))

    # Step 2: Clone and Build Tree
    if st.button("📥 Clone & Build Tree"):
        with st.spinner("Cloning and building file tree..."):
            clone_resp = requests.post("http://localhost:8000/agentic_clone", json={"url": github_url})
            repo_path = clone_resp.json().get("result", "")
            tree_resp = requests.post("http://localhost:8000/build_tree_structure", json={"repo_dir": repo_path})
            st.subheader("📁 File Tree")
            st.code(tree_resp.json().get("result", "No tree generated"))

    # Step 3: Summarize Repository
    if st.button("📝 Summarize Repository"):
        with st.spinner("Summarizing repository..."):
            summary_resp = requests.post("http://localhost:8000/summairize_repo", json={"repo_url": github_url})
            st.subheader("📄 Summary")
            st.write(summary_resp.json().get("result", "No summary available"))

    # Step 4: Analyze Structure
    if st.button("🔍 Analyze Structure"):
        with st.spinner("Analyzing repository structure..."):
            analyze_resp = requests.post("http://localhost:8000/analyze_repo", json={
                "repo_dir": repo_path,
                "tree_structure": tree_resp.json().get("result", "")
            })
            st.subheader("🧩 Analysis")
            st.write(analyze_resp.json().get("result", "No analysis available"))

    # Step 5: Generate Documentation
    if st.button("📚 Generate Documentation"):
        with st.spinner("Generating markdown documentation..."):
            doc_resp = requests.post("http://localhost:8000/generate_doc", json={
                "data": {
                    "repo_url": github_url,
                    "repo_dir": repo_path,
                    "tree_structure": tree_resp.json().get("result", ""),
                    "summary": summary_resp.json().get("result", "")
                }
            })
            st.subheader("📘 Markdown Documentation")
            st.code(doc_resp.json().get("result", "No documentation generated"), language="markdown")