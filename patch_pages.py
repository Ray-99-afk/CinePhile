import re
import os

CSS_ADD = """
        /* Profile Panel */
        .profile-btn { display:flex; align-items:center; gap:10px; cursor:pointer; background:rgba(255,255,255,.05); padding:6px 14px 6px 6px; border-radius:30px; border:1px solid rgba(255,215,0,.3); transition:all .3s ease; margin-bottom: 8px;}
        .profile-btn:hover { background:rgba(255,215,0,.15); border-color:var(--gold); }
        .profile-avatar-sm { width:32px; height:32px; border-radius:50%; background:var(--gold); color:#000; display:flex; align-items:center; justify-content:center; font-family:'Bebas Neue',sans-serif; font-size:1.1rem; }
        .profile-name-sm { font-family:'Poppins',sans-serif; font-size:.85rem; color:var(--text); letter-spacing:1px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:80px; }

        .profile-panel { position:fixed; top:0; right:-400px; width:400px; height:100dvh; background:var(--surface); z-index:2000; transition:right .4s cubic-bezier(.25,1,.5,1); display:flex; flex-direction:column; box-shadow:-10px 0 30px rgba(0,0,0,.5); overflow-y:auto; overflow-x:hidden; }
        .profile-panel.open { right:0; }
        .profile-overlay { position:fixed; inset:0; background:rgba(0,0,0,.6); z-index:1999; display:none; backdrop-filter:blur(3px); }
        .profile-overlay.open { display:block; }
        
        .profile-hdr { padding:30px; display:flex; align-items:center; justify-content:flex-end; }
        .profile-close-btn { background:none; border:none; color:var(--text-dim); font-size:1.8rem; cursor:pointer; transition:color .3s; }
        .profile-close-btn:hover { color:var(--danger); }
        
        .profile-body { padding:40px 30px; flex:1; display:flex; flex-direction:column; align-items:center; padding-top:0;}
        .profile-avatar-lg { width:100px; height:100px; border-radius:50%; background:var(--gold); color:#000; display:flex; align-items:center; justify-content:center; font-family:'Bebas Neue',sans-serif; font-size:3.5rem; margin-bottom:20px; border:2px solid #fff; box-shadow:0 0 20px rgba(255,215,0,.3); margin-bottom:0; overflow:hidden;}
        
        .profile-input-group { width:100%; margin-bottom:20px; text-align:left;}
        .profile-input-group label { display:block; font-family:'Poppins',sans-serif; font-size:.75rem; color:var(--text-dim); margin-bottom:8px; text-transform:uppercase; letter-spacing:1px; }
        .profile-input { background:var(--surface2, #1c1c28); border:1px solid rgba(255,215,0,.3); color:#fff; padding:12px 20px; font-family:'Poppins',sans-serif; font-size:1rem; border-radius:4px; outline:none; width:100%; transition:all .3s; max-width: 100%; box-sizing: border-box;}
        
        .profile-footer { padding:20px 30px; border-top:1px solid rgba(255,255,255,.05); margin-top:auto;}
        
        .hidden { display:none !important; }
"""

HTML_NAV_RIGHT = """        <div class="nav-right" style="display:flex; flex-direction: column; align-items: flex-end; gap: 5px;">
            <div class="profile-btn" onclick="toggleProfile()">
                <div class="profile-avatar-sm" id="nav-initial">?</div>
                <span class="profile-name-sm" id="nav-username">Welcome</span>
            </div>
            <button class="watchlist-btn" onclick="toggleWL()" style="display:flex; align-items:center; gap:6px; background:none; border:1px solid rgba(255,215,0,.4); color:var(--gold); padding:4px 12px; cursor:pointer; font-family:'Roboto Condensed',sans-serif; font-size:.75rem; letter-spacing:1px; text-transform:uppercase; transition:all .3s; border-radius:2px;">
                <i class='bx bx-bookmark'></i> WATCHLIST
                <span class="wl-count" id="wl-count" style="background:var(--gold); color:#000; font-size:.65rem; font-weight:700; width:15px; height:15px; border-radius:50%; display:none; align-items:center; justify-content:center;">0</span>
            </button>
        </div>"""

HTML_DRAWER = """
    <!-- Profile Overlay & Panel -->
    <div class="profile-overlay" id="profile-overlay" onclick="toggleProfile()"></div>
    <div class="profile-panel" id="profile-panel" style="z-index:99999;">
        <div class="profile-hdr">
            <button class="profile-close-btn" onclick="toggleProfile()"><i class='bx bx-x'></i></button>
        </div>
        <div class="profile-body">
            <div style="position:relative; margin-bottom:30px;">
                <div class="profile-avatar-lg" id="profile-avatar-lg">?</div>
                <button onclick="changeAvatar()" style="position:absolute; bottom:0; right:0; background:var(--gold); border:none; color:#000; width:34px; height:34px; border-radius:50%; display:flex; align-items:center; justify-content:center; cursor:pointer; box-shadow:0 0 10px rgba(255,215,0,.5); font-size:1.2rem; transition:transform .3s; z-index: 2;">
                    <i class='bx bxs-camera'></i>
                </button>
            </div>
            
            <div class="profile-input-group">
                <label>Character Name</label>
                <input type="text" id="profile-name-input" class="profile-input" placeholder="Enter new name...">
            </div>
            
            <button id="btn-save-profile" class="hidden" style="width:100%; font-size:1rem; padding:10px; justify-content:center; display:flex; align-items:center; gap:6px; background:none; border:1px solid rgba(255,215,0,.4); color:var(--gold); cursor:pointer; font-family:'Roboto Condensed',sans-serif; letter-spacing:1px; text-transform:uppercase; transition:all .3s; border-radius:4px; margin-top:20px;" onclick="saveProfile()"><i class='bx bx-save'></i> SAVE CHANGES</button>
        </div>
        <div class="profile-footer">
            <button style="width:100%; border:1px solid var(--danger); background:none; color:var(--danger); font-size:1rem; padding:10px; justify-content:center; display:flex; align-items:center; gap:6px; cursor:pointer; font-family:'Roboto Condensed',sans-serif; letter-spacing:1px; text-transform:uppercase; transition:all .3s; border-radius:4px;" onclick="logout()">
                <i class='bx bx-log-out-circle'></i> LOGOUT
            </button>
        </div>
    </div>
"""

JS_FIREBASE = """
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
        import { getAuth, updateProfile } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";
        const firebaseConfig = {
            apiKey: "AIzaSyA81Gb34RwpjVU1w3l5eAxktd3BribOJzo",
            authDomain: "cinephile-binge.firebaseapp.com",
            projectId: "cinephile-binge"
        };
        const app = initializeApp(firebaseConfig);
        const auth = getAuth(app);
        window.fbUpdateProfile = async (newName, newPhotoUrl) => {
            if(!auth || !auth.currentUser) return false;
            try {
                await updateProfile(auth.currentUser, { displayName: newName, photoURL: newPhotoUrl || "" });
                return true;
            } catch (e) { return false; }
        };
    </script>
"""

JS_LOGIC = """
    let meName = localStorage.getItem('cinephile_user_name') || 'PLAYER';
    let currentAvatarUrl = localStorage.getItem('cinephile_avatar') || '';

    function getLoadName() {
        meName = localStorage.getItem('cinephile_user_name') || 'PLAYER';
        currentAvatarUrl = localStorage.getItem('cinephile_avatar') || '';
        
        if(document.getElementById('nav-username')) {
            document.getElementById('nav-username').textContent = meName;
            document.getElementById('profile-name-input').value = meName;
            
            if (currentAvatarUrl) {
                document.getElementById('nav-initial').innerHTML = `<img src="${currentAvatarUrl}" style="width:100%; height:100%; border-radius:50%; object-fit:cover;">`;
                document.getElementById('profile-avatar-lg').innerHTML = `<img src="${currentAvatarUrl}" style="width:100%; height:100%; border-radius:50%; object-fit:cover;">`;
            } else {
                document.getElementById('nav-initial').textContent = meName.charAt(0).toUpperCase();
                document.getElementById('profile-avatar-lg').textContent = meName.charAt(0).toUpperCase();
            }
        }
    }

    function changeAvatar() {
        const url = prompt("Enter an Image URL for your new avatar:", currentAvatarUrl);
        if (url !== null) {
            localStorage.setItem('cinephile_avatar', url.trim());
            const btn = document.getElementById('btn-save-profile');
            if(btn) btn.classList.remove('hidden');
            getLoadName();
        }
    }

    function toggleProfile() {
        document.getElementById('profile-panel').classList.toggle('open');
        document.getElementById('profile-overlay').classList.toggle('open');
        getLoadName();
        const btn = document.getElementById('btn-save-profile');
        if(btn) btn.classList.add('hidden');
    }

    async function saveProfile() {
        const newName = document.getElementById('profile-name-input').value.trim();
        const avatarUrl = localStorage.getItem('cinephile_avatar') || '';
        
        if(!newName) { alert("Name cannot be empty!"); return; }
        
        localStorage.setItem('cinephile_user_name', newName); 
        getLoadName(); 

        if(window.fbUpdateProfile) {
            await window.fbUpdateProfile(newName, avatarUrl);
        }
        document.getElementById('btn-save-profile').classList.add('hidden');
        toggleProfile();
    }

    function logout() { localStorage.removeItem("cinephile_user_name"); window.location.href="02_login.html"; }

    document.addEventListener('DOMContentLoaded', () => {
        getLoadName();
        const input = document.getElementById('profile-name-input');
        if(input) {
            input.addEventListener('input', () => {
                const btn = document.getElementById('btn-save-profile');
                if (input.value.trim() !== meName) {
                    btn.classList.remove('hidden');
                } else {
                    btn.classList.add('hidden');
                }
            });
        }
    });

"""

def patch_file(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. CSS
    if '.profile-btn' not in content:
        content = re.sub(r'(</style>)', CSS_ADD + r'\1', content)
        
    # 2. HTML Nav
    if '<div class="nav-right">' in content:
        content = re.sub(r'<div class="nav-right">.*?</button>\s*</div>', HTML_NAV_RIGHT, content, flags=re.DOTALL)
    elif 'nav-hint' in content and 'nav-right' not in content: # dashboard
        # Add nav-right to dashboard right aligned
        content = re.sub(r'(<div class="nav-spacer"></div>)\s*(</nav>)', HTML_NAV_RIGHT + r'\n\2', content)

    # 3. HTML Drawer
    if 'profile-panel' not in content:
        content = re.sub(r'(<script>)', HTML_DRAWER + r'\n\1', content, count=1)
        
    # 4. JS Firebase
    if 'window.fbUpdateProfile' not in content:
        content = re.sub(r'(</body>)', JS_FIREBASE + r'\n\1', content)
        
    # 5. JS Logic
    if 'getLoadName()' not in content:
        if 'const navUName' in content: 
            # remove old logical block in series/movies
            content = re.sub(r'// Logic for Username and Logout.*?const urlParams', JS_LOGIC + r'\n    const urlParams', content, flags=re.DOTALL)
        else:
            # Dashboard
            content = re.sub(r'(</script>\s*</body>)', JS_LOGIC + r'\1', content)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

for p in [r'c:\Users\aryan\OneDrive\Documents\Projects\CinePhile\03_dashboard.html', r'c:\Users\aryan\OneDrive\Documents\Projects\CinePhile\04_movies.html', r'c:\Users\aryan\OneDrive\Documents\Projects\CinePhile\05_series.html']:
    patch_file(p)
