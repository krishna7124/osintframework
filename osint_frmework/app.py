import streamlit as st
import json, re
from pathlib import Path
from fuzzywuzzy import fuzz
from typing import List, Dict, Tuple

# ---------- CONFIG ----------
st.set_page_config(
    page_title="OSINT Toolkit",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- JAVASCRIPT FOR WIDTH DETECTION ----------
import streamlit.components.v1 as components

# Inject JavaScript to detect screen width and set session state
components.html(
    """
    <script>
        (function() {
            const width = window.innerWidth;
            let message;
            if (width <= 500) {
                message = { type: 'SET_MOBILE', value: 'phone' }; // 3 cards on phones
            } else if (width <= 1000) {
                message = { type: 'SET_MOBILE', value: 'tablet' }; // 2 cards on tablets
            } else {
                message = { type: 'SET_MOBILE', value: 'desktop' }; // 3 cards on desktops
            }
            window.parent.postMessage(message, '*');
        })();
    </script>
    """,
    height=0,
)

# Update session state based on message (simplified handling)
if 'is_mobile' not in st.session_state:
    st.session_state.is_mobile = 'desktop'  # Default to desktop

# ---------- DATA LOADING ----------
@st.cache_data(ttl=3600, show_spinner="Loading tools...")
def load_tools() -> Dict:
    try:
        path = Path(__file__).parent / "data" / "osint_tools.json"
        if not path.exists():
            st.error("Data file not found. Please ensure data/osint_tools.json exists.")
            st.stop()  # Stop execution if data is missing
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            for ci, c in enumerate(data.get("categories", [])):
                for ti, t in enumerate(c.get("tools", [])):
                    t["uid"] = f"{ci}_{ti}"
                    t["tags"] = t.get("tags", [])
                    t["category"] = c["name"]
            return data
    except json.JSONDecodeError:
        st.error("Invalid JSON format in osint_tools.json")
        st.stop()
    except Exception as e:
        st.error(f"Error loading tools: {str(e)}")
        st.stop()

tools = load_tools()

# ---------- ICONS ----------
icons = {
    "Training": "📚",
    "Documentation / Evidence Capture": "📑",
    "OpSec": "🔒",
    "Threat Intelligence": "🕵️‍♂️",
    "Exploits & Advisories": "⚠️",
    "Malicious File Analysis": "🛡️",
    "AI Tools": "🤖",
    "Tools": "🛠️",
    "Encoding / Decoding": "🔐",
    "Classifieds": "📢",
    "Digital Currency": "💸",
    "Dark Web": "🌑",
    "Terrorism": "🚨",
    "Mobile Emulation": "📱",
    "Metadata": "🔍",
    "Language Translation": "🌐",
    "Archives": "📦",
    "Forums / Blogs / IRC": "💬",
    "Search Engines": "🔎",
    "Geolocation Tools / Maps": "📍",
    "Transportation": "🚗",
    "Business Records": "🏢",
    "Public Records": "📜",
    "Telephone Numbers": "📞",
    "Dating": "❤️",
    "People Search Engines": "👥",
    "Instant Messaging": "💬",
    "Social Networks": "🌐",
    "Images / Videos / Docs": "🖼️",
    "IP & MAC Address": "🌐",
    "Domain Name": "🌍",
    "Email Address": "📧",
    "Username": "👤"
}

def get_category_icon(category_name: str) -> str:
    return icons.get(category_name, "🛠️")

# ---------- CSS & STYLING (Enhanced) ----------
st.markdown(
    """
    <style>
    :root {
        --border: #3a3a3a;
        --accent: #8be9fd;
        --shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
        --header-bg: linear-gradient(135deg, #2a2a2a, #4a4a4a);
        --header-text: #ffffff;
        --love-color: #ff6b6b;
        --logo-size: 50px;
        --footer-bg: linear-gradient(135deg, #2a2a2a, #1a1a1a);
    }

    .header {
        background: var(--header-bg);
        padding: 1.5rem;
        text-align: center;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
        animation: fadeIn 1s ease-in-out;
        position: relative;
        overflow: hidden;
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    .header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(139, 233, 253, 0.2) 0%, transparent 70%);
        animation: pulse 6s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(0); }
        100% { transform: scale(1); }
    }

    .header .logo {
        width: var(--logo-size);
        height: var(--logo-size);
        # background: url('https://via.placeholder.com/50') no-repeat center;
        background-size: cover;
        margin: 0 auto 0.75rem;
        border-radius: 50%;
        border: 2px solid var(--accent);
    }

    .header h1 {
        color: var(--header-text);
        font-size: 2.8rem;
        margin: 0;
        font-weight: 900;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.3);
    }

    .header p {
        color: var(--header-text);
        font-size: 1.2rem;
        margin: 0.5rem 0 0;
        opacity: 0.9;
        font-style: italic;
    }

    .header .love-credit {
        font-size: 0.9rem;
        color: var(--love-color);
        margin-top: 0.75rem;
        font-style: italic;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
    }

    .tool-card {
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 0.8rem;
        box-shadow: var(--shadow);
        margin-bottom: 1rem;
        max-width: 300px;
    }

    .tool-icon {
        font-size: 1.2rem;
        margin-right: 0.6rem;
        color: var(--accent);
    }

    .tool-title {
        font-weight: 800;
        font-size: 1rem;
        margin: 0;
    }

    .tool-category {
        font-size: 0.75rem;
        margin-bottom: 0.4rem;
    }

    .tool-description {
        font-size: 0.9rem;
        line-height: 1.5;
    }

    .tool-link {
            display: inline-block;
            padding: 0.3rem 0.6rem;
            text-decoration: none;
            border-radius: 4px;
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--accent);
            border: 1px solid var(--accent);
            background-color: rgba(139, 233, 253, 0.2);
        }

        @media (prefers-color-scheme: light) {
            .tool-link {
                background-color: rgba(0, 119, 182, 0.2);
                color: #0077b6;
            }
        }

        .tool-link:hover {
            background-color: var(--accent);
            color: #ff0000;
        }

        .tool-badge {
            font-size: 0.65rem;
            font-weight: 500;
            padding: 0.15rem 0.5rem;
            border-radius: 6px;
            border: 1px solid var(--accent);
            color: #000000;
            background-color: var(--accent);
        }

    mark {
        background-color: rgba(255, 121, 198, 0.3);
        color: inherit;
        padding: 0.1em 0.3em;
        border-radius: 3px;
    }

    .st.Selectbox > div > div, .stTextInput > div > div > input {
        border-color: var(--border) !important;
        border-radius: 8px !important;
    }

    .footer {
        background: var(--footer-bg);
        padding: 1.5rem 0;
        text-align: center;
        border-radius: 8px;
        box-shadow: var(--shadow);
        margin-top: 2rem;
        color: var(--header-text);
        opacity: 0.9;
    }

    .footer a {
        color: var(--accent);
        text-decoration: none;
        margin: 0 0.5rem;
        font-weight: 500;
    }

    .footer a:hover {
        text-decoration: underline;
        color: #a3e4ff;
    }

    .footer small {
        display: block;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- HEADER ----------
st.markdown(
    """
    <div class="header">
        <div class="logo"></div>
        <h1>OSINT Toolkit</h1>
        <p>Your Ultimate Open-Source Intelligence Companion</p>
        <div class="love-credit">Made with ❤️ by Krishna Bhatt</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("🔍 OSINT Toolkit")
    st.markdown("---")
    
    cats = ["All"] + [c["name"] for c in tools["categories"]]
    sel_cat = st.selectbox(
        "Category",
        cats,
        key="category_filter",
        help="Filter tools by category"
    )
    
    q = st.text_input(
        "Search tools",
        placeholder="Search by name or description...",
        key="search_input",
        help="Search by name or description"
    )
    
    st.markdown("---")
    total_tools = sum(len(c["tools"]) for c in tools["categories"])
    st.markdown(
        f"<small>Found {len(tools['categories'])} categories with {total_tools} tools</small>",
        unsafe_allow_html=True
    )

# ---------- SEARCH FUNCTION ----------
@st.cache_data(ttl=300, show_spinner=False)
def search_tools(query: str, selected_category: str, selected_tags: List[str]) -> List[Tuple[str, Dict, float]]:
    query = query.lower().strip() if query else ""
    out = []
    
    for c in tools["categories"]:
        if selected_category != "All" and c["name"] != selected_category:
            continue
            
        for t in c["tools"]:
            if selected_tags and selected_tags != ["No tags available"] and not any(tag in t.get("tags", []) for tag in selected_tags):
                continue
                
            score = 100.0
            if query:
                tags_text = " ".join(t.get("tags", []))
                score = max(
                    fuzz.partial_ratio(query, t["name"].lower()),
                    fuzz.partial_ratio(query, t["description"].lower()),
                    fuzz.partial_ratio(query, c["name"].lower()),
                    fuzz.partial_ratio(query, tags_text.lower()),
                )
                if score < 65:
                    continue
                    
            out.append((c["name"], t, score))
    
    return sorted(out, key=lambda x: (-x[2], x[1]["name"]))

# ---------- MAIN CONTENT ----------
hits = search_tools(q, sel_cat, [])  # Pass empty tag list since tag filtering is removed

if not hits:
    st.info("No tools found matching your criteria. Try adjusting your filters or search terms.")
else:
    # Determine number of columns based on screen size detected by JavaScript
    if st.session_state.is_mobile == 'phone':
        num_columns = 3  # 3 cards on phones
    elif st.session_state.is_mobile == 'tablet':
        num_columns = 2  # 2 cards on tablets
    else:  # desktop
        num_columns = 3  # 3 cards on desktops

    # Calculate number of rows needed
    num_rows = (len(hits) + num_columns - 1) // num_columns

    # Render cards in rows and columns
    for row in range(num_rows):
        with st.container():
            cols = st.columns(num_columns)
            for col in range(num_columns):
                index = row * num_columns + col
                if index < len(hits):
                    cat, t, score = hits[index]
                    title = re.sub(re.escape(q or ""), f"<mark>{q}</mark>", t["name"], flags=re.I) if q else t["name"]
                    desc = re.sub(re.escape(q or ""), f"<mark>{q}</mark>", t["description"], flags=re.I) if q else t["description"]

                    with cols[col]:
                        st.markdown(f"""
                            <div class="tool-card">
                                <div style="display: flex; align-items: center; gap: 0.4rem;">
                                    <div class="tool-icon">{get_category_icon(cat)}</div>
                                    <h3 class="tool-title">{title}</h3>
                                </div>
                                <div class="tool-category">
                                    <span class="tool-badge">{cat}</span>
                                </div>
                                <p class="tool-description">{desc}</p>
                                <div style="margin-top: 0.6rem;">
                                    <a href="{t['url']}" target="_blank" class="tool-link">🔗 Visit Tool</a>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown(
    """
    <div class="footer">
        <div>
            <a href="https://github.com/your-username/osint-toolkit/issues" target="_blank">Feedback</a>
             • 
            <a href="https://github.com/krishna7124" target="_blank">GitHub</a>
             • 
            <a href="mailto:krishnabhatt268@gmail.com">Contact</a>
        </div>
        <small>OSINT Toolkit • Updated: July 20, 2025, 01:02 PM IST</small>
    </div>
    """,
    unsafe_allow_html=True,
)