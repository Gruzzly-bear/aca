import os
import glob
import re
import math

# --- CONFIGURATION ---
CONTENT_DIR = "files"

if not os.path.exists(CONTENT_DIR):
    print(f"Error: Could not find '{CONTENT_DIR}' folder.")
    exit()

local_files = {f.lower(): f for f in os.listdir(CONTENT_DIR) if f.endswith(".html")}
series_buckets = {}

for filename in local_files.values():
    match = re.fullmatch(r'scp-(\d+)\.html', filename.lower())
    if match:
        num = int(match.group(1))
        s_num = math.floor(num / 1000) + 1
        if s_num not in series_buckets: series_buckets[s_num] = []
        series_buckets[s_num].append({"file": filename, "id": f"SCP-{str(num).zfill(3)}", "sort": num})

def make_page(title, out_f, items, series_idx):
    clearance = "Level 2 (Restricted)" if series_idx < 4 else "Level 4 (Top Secret)"
    if series_idx == 1: clearance = "Level 1 (Confidential)"
    
    items.sort(key=lambda x: x["sort"])
    links = "".join([f'<a href="files/{i["file"]}" target="viewer" class="item" onclick="toggleSidebar()">{i["id"]}</a>' for i in items])
    
    html = f"""<!DOCTYPE html><html><head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            :root {{ --accent: #d32f2f; --bg: #121212; }}
            body {{ font-family: 'Segoe UI', sans-serif; background: var(--bg); color: #eee; display: flex; margin: 0; height: 100vh; overflow: hidden; }}
            
            /* Sidebar Styling */
            #sidebar {{ width: 320px; background: #1a1a1a; display: flex; flex-direction: column; border-right: 1px solid #333; transition: 0.3s; z-index: 1000; }}
            .header {{ padding: 20px; background: #b71c1c; }}
            .badge {{ display: inline-block; padding: 4px 8px; background: #000; color: var(--accent); font-size: 0.7rem; font-weight: bold; border: 1px solid var(--accent); margin-top: 10px; text-transform: uppercase; }}
            #list {{ flex: 1; overflow-y: auto; background: #111; }}
            .item {{ display: block; padding: 15px 20px; color: #888; text-decoration: none; border-bottom: 1px solid #222; font-size: 1rem; }}
            .item:hover {{ background: #222; color: #fff; border-left: 4px solid var(--accent); }}
            
            /* Main Content View */
            #main {{ flex: 1; position: relative; display: flex; flex-direction: column; }}
            iframe {{ width: 100%; height: 100%; border: none; background: #222; }}

            /* Mobile Toggle Button */
            #mobile-toggle {{ 
                display: none; position: fixed; bottom: 20px; right: 20px; 
                background: var(--accent); color: white; border: none; 
                border-radius: 50%; width: 60px; height: 60px; font-weight: bold; 
                box-shadow: 0 4px 10px rgba(0,0,0,0.5); z-index: 1001; cursor: pointer;
            }}

            /* MOBILE RESPONSIVENESS */
            @media (max-width: 768px) {{
                #sidebar {{ position: fixed; left: -320px; height: 100%; }}
                #sidebar.open {{ left: 0; width: 85%; }}
                #mobile-toggle {{ display: block; }}
            }}
        </style>
    </head><body>
        <button id="mobile-toggle" onclick="toggleSidebar()">MENU</button>
        <div id="sidebar">
            <div class="header">
                <h2 style="margin:0; font-size: 1.2rem;">{title}</h2>
                <div class="badge">{clearance}</div>
                <a href="index.html" style="display:block; color:white; font-size:0.8rem; margin-top:10px; opacity:0.6; text-decoration:none;">← MAIN MENU</a>
            </div>
            <div id="list">{links}</div>
        </div>
        <div id="main"><iframe name="viewer"></iframe></div>
        <script>
            function toggleSidebar() {{
                document.getElementById('sidebar').classList.toggle('open');
            }}
        </script>
    </body></html>"""
    with open(out_f, "w", encoding="utf-8") as f: f.write(html)

for s, data in series_buckets.items():
    make_page(f"SERIES {s}", f"series_{s}.html", data, s)
print("Mobile optimization complete.")