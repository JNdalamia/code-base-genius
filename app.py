import streamlit as st
import requests

st.set_page_config(page_title="Codebase Genius", layout="wide")

# Initialize session state
for key in ["repo_path", "tree_structure", "summary", "analysis", "documentation"]:
    if key not in st.session_state:
        st.session_state[key] = ""

st.title("🧠 Codebase Genius")

# Sidebar input
st.sidebar.header("🔗 Repository Input")
github_url = st.sidebar.text_input("Enter GitHub Repository URL", value="https://github.com/jaclang/jac")

# Tabs for each step
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "✅ Verify Repo",
    "📥 Clone & Tree",
    "📝 Summarize",
    "🔍 Analyze",
    "📚 Generate Docs"
])

with tab1:
    st.header("✅ Verify Repository")
    if st.button("Verify"):
        with st.spinner("Verifying repository..."):
            response = requests.post("http://localhost:8000/verify_repo", json={"url": github_url})
            st.write("Verification Result:", response.json().get("result", "No response"))

with tab2:
    st.header("📥 Clone & Build Tree")
    if st.button("Clone & Build"):
        with st.spinner("Cloning and building file tree..."):
            clone_resp = requests.post("http://localhost:8000/agentic_clone", json={"url": github_url})
            st.session_state.repo_path = clone_resp.json().get("result", "")
            tree_resp = requests.post("http://localhost:8000/build_tree_structure", json={"repo_dir": st.session_state.repo_path})
            st.session_state.tree_structure = tree_resp.json().get("result", "")
            st.subheader("📁 File Tree")
            st.code(st.session_state.tree_structure)

with tab3:
    st.header("📝 Summarize Repository")
    if st.button("Summarize"):
        with st.spinner("Summarizing repository..."):
            summary_resp = requests.post("http://localhost:8000/summarize_repo", json={"repo_url": github_url})
            st.session_state.summary = summary_resp.json().get("result", "")
            st.subheader("📄 Summary")
            st.write(st.session_state.summary)

with tab4:
    st.header("🔍 Analyze Structure")
    if st.button("Analyze"):
        if not st.session_state.repo_path or not st.session_state.tree_structure:
            st.warning("Please run Clone & Build Tree first.")
        else:
            with st.spinner("Analyzing repository structure..."):
                analyze_resp = requests.post("http://localhost:8000/analyze_repo", json={
                    "repo_dir": st.session_state.repo_path,
                    "tree_structure": st.session_state.tree_structure
                })
                st.session_state.analysis = analyze_resp.json().get("result", "")
                st.subheader("🧩 Analysis")
                st.write(st.session_state.analysis)

with tab5:
    st.header("📚 Generate Documentation")
    if st.button("Generate Docs"):
        if not github_url or not st.session_state.repo_path or not st.session_state.tree_structure or not st.session_state.summary:
            st.warning("Please complete all previous steps before generating documentation.")
        else:
            with st.spinner("Generating markdown documentation..."):
                doc_resp = requests.post("http://localhost:8000/generate_doc", json={
                    "data": {
                        "repo_url": github_url,
                        "repo_dir": st.session_state.repo_path,
                        "tree_structure": st.session_state.tree_structure,
                        "summary": st.session_state.summary,
                        "analysis": st.session_state.analysis
                    }
                })
                st.session_state.documentation = doc_resp.json().get("result", "")
                st.subheader("📘 Markdown Documentation")
                st.code(st.session_state.documentation, language="markdown")

                # Export as file
                st.download_button(
                    label="📥 Download Markdown",
                    data=st.session_state.documentation,
                    file_name="documentation.md",
                    mime="text/markdown"
                )

# Optional: Reset session
if st.sidebar.button("🔄 Reset Session"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()