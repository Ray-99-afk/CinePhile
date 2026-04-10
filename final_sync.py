import os
import re

# Comprehensive CSS including Profile Panel and Friends Panel
FULL_PANEL_CSS = """
        /* Profile & Friends Panels Common */
        .profile-btn, .friend-nav-btn { display:flex; align-items:center; gap:10px; cursor:pointer; background:rgba(255,255,255,.05); padding:6px 14px 6px 6px; border-radius:30px; border:1px solid rgba(255,215,0,.3); transition:all .3s ease; }
        .profile-btn:hover, .friend-nav-btn:hover { background:rgba(255,215,0,.1); border-color:var(--gold); }
        .profile-avatar-sm { width:32px; height:32px; border-radius:50%; background:var(--gold); color:#000; display:flex; align-items:center; justify-content:center; font-family:'Bebas Neue'; font-size:1.1rem; overflow:hidden; }
        .profile-avatar-sm img { width:100%; height:100%; object-fit:cover; }
        .profile-name-sm { font-family:'Poppins'; font-size:.85rem; color:#fff; letter-spacing:1px; max-width:80px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }

        .profile-panel, .friend-panel { position:fixed; top:0; width:400px; height:100dvh; background:#080808; z-index:2000; transition:all .4s cubic-bezier(.25,1,.5,1); display:flex; flex-direction:column; box-shadow:0 0 30px rgba(0,0,0,.8); overflow-y:auto; border-left:1px solid rgba(255,255,255,.05); }
        .profile-panel { right:-400px; }
        .profile-panel.open { right:0; }
        .friend-panel { left:-400px; border-left:none; border-right:1px solid rgba(255,255,255,.05); }
        .friend-panel.open { left:0; }

        .panel-overlay { position:fixed; inset:0; background:rgba(0,0,0,.7); z-index:1999; display:none; backdrop-filter:blur(4px); }
        .panel-overlay.open { display:block; }

        .panel-hdr { padding:30px; display:flex; align-items:center; justify-content:space-between; border-bottom:1px solid rgba(255,255,255,.05); }
        .panel-hdr h2 { font-family:'Bebas Neue'; font-size:2rem; letter-spacing:4px; margin:0; }
        .panel-close-btn { background:none; border:none; color:#999; font-size:1.8rem; cursor:pointer; transition:color .3s; }
        .panel-close-btn:hover { color:#e50914; }

        .profile-body, .friend-list { padding:40px 30px; flex:1; display:flex; flex-direction:column; align-items:center; }
        .profile-avatar-lg { width:100px; height:100px; border-radius:50%; background:var(--gold); color:#000; display:flex; align-items:center; justify-content:center; font-family:'Bebas Neue'; font-size:3.5rem; border:2px solid #fff; box-shadow:0 0 20px rgba(255,215,0,.3); overflow:hidden; margin-bottom:0; }
        .profile-avatar-lg img { width:100%; height:100%; object-fit:cover; }

        .profile-input-group { width:100%; margin:25px 0; text-align:left;}
        .profile-input-group label { display:block; font-family:'Poppins'; font-size:.75rem; color:#999; margin-bottom:8px; text-transform:uppercase; letter-spacing:1px; }
        .profile-input { background:rgba(255,255,255,.05); border:1px solid rgba(255,215,0,.3); color:#fff; padding:12px 18px; font-family:'Poppins'; font-size:1rem; border-radius:4px; outline:none; width:100%; }

        .save-btn { width:100%; padding:12px; background:none; border:1px solid var(--gold); color:var(--gold); font-family:'Roboto Condensed'; font-size:.9rem; letter-spacing:2px; text-transform:uppercase; cursor:pointer; border-radius:4px; transition:all .3s; display:flex; align-items:center; justify-content:center; gap:8px; }
        .save-btn:hover { background:rgba(255,215,0,.1); }
        
        .logout-btn { width:100%; padding:12px; background:none; border:1px solid #e50914; color:#e50914; font-family:'Roboto Condensed'; font-size:.9rem; letter-spacing:2px; text-transform:uppercase; cursor:pointer; border-radius:4px; transition:all .3s; }
        .logout-btn:hover { background:rgba(229,9,20,.1); }

        /* Friends Items */
        .friend-list { width:100%; align-items:stretch; padding-top:20px; }
        .friend-item { display:flex; align-items:center; gap:15px; padding:12px; background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.05); border-radius:4px; transition:all .3s; margin-bottom:12px; }
        .friend-item:hover { border-color:rgba(168,85,247,.4); }
        .friend-avatar { width:42px; height:42px; border-radius:50%; background:#a855f7; display:flex; align-items:center; justify-content:center; color:#fff; font-family:'Bebas Neue'; font-size:1.4rem; overflow:hidden;}
        .friend-avatar img { width:100%; height:100%; object-fit:cover; }
        .friend-name { font-family:'Poppins'; font-size:.9rem; font-weight:500; color:#fff; flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }

        .friend-add-btn { width:100%; padding:12px; background:none; border:1px solid #a855f7; color:#a855f7; font-family:'Roboto Condensed'; font-size:.9rem; letter-spacing:1px; cursor:pointer; border-radius:4px; transition:all .3s; margin-top:auto; }
        .friend-add-btn:hover { background:rgba(168,85,247,.1); color:#fff; }

        .modal-bg { position:fixed; inset:0; background:rgba(0,0,0,.85); z-index:3000; display:none; align-items:center; justify-content:center; backdrop-filter:blur(8px); }
        .modal-bg.open { display:flex; }
        .friend-modal { background:#111; width:90%; max-width:400px; padding:40px 30px; border-radius:8px; border:1px solid rgba(168,85,247,.3); text-align:center; position:relative; }
        .friend-modal h3 { font-family:'Bebas Neue'; font-size:2.5rem; letter-spacing:2px; margin-bottom:10px; }
        .friend-submit { width:100%; padding:14px; background:#a855f7; border:none; color:#fff; font-family:'Bebas Neue'; font-size:1.2rem; letter-spacing:2px; border-radius:4px; cursor:pointer; transition:all .3s; }
        .friend-submit:hover { transform:translateY(-2px); box-shadow:0 10px 20px rgba(168,85,247,.3); }

        .hidden { display:none !important; }
"""

JS_MODULE_TEMPLATE = """
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
        import { getAuth, updateProfile } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";
        import { getDatabase, ref, set, get, child } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-database.js";

        const firebaseConfig = {
            apiKey: "AIzaSyA81Gb34RwpjVU1w3l5eAxktd3BribOJzo",
            authDomain: "cinephile-binge.firebaseapp.com",
            databaseURL: "https://cinephile-binge-default-rtdb.firebaseio.com",
            projectId: "cinephile-binge"
        };
        const app = initializeApp(firebaseConfig);
        const auth = getAuth(app);
        const db = getDatabase(app);

        // --- Profile Core ---
        window.fbUpdateProfile = async (newName, newPhotoUrl) => {
            if(!auth || !auth.currentUser) return false;
            try {
                await updateProfile(auth.currentUser, { displayName: newName, photoURL: newPhotoUrl || "" });
                const lowerName = newName.trim().toLowerCase();
                if(lowerName) await set(ref(db, `users_by_name/${lowerName}`), { uid: auth.currentUser.uid, name: newName, avatar: newPhotoUrl || '' });
                return true;
            } catch (e) { return false; }
        };

        window.logout = () => { localStorage.removeItem('cinephile_user_name'); window.location.href='02_login.html'; };

        // --- Friends UI Actions ---
        window.toggleProfile = () => {
            const p = document.getElementById('profile-panel');
            const over = document.getElementById('panel-overlay');
            p.classList.toggle('open');
            over.classList.toggle('open');
            if(p.classList.contains('open')) {
                document.getElementById('friend-panel').classList.remove('open');
                getLoadName();
            }
        };

        window.toggleFriendsPanel = () => {
            const p = document.getElementById('friend-panel');
            const over = document.getElementById('panel-overlay');
            p.classList.toggle('open');
            over.classList.toggle('open');
            if(p.classList.contains('open')) {
                document.getElementById('profile-panel').classList.remove('open');
                loadFriends();
            }
        };

        window.closeAllPanels = () => {
             document.querySelectorAll('.profile-panel, .friend-panel, .panel-overlay').forEach(el=>el.classList.remove('open'));
        };

        window.openAddFriendModal = () => {
            document.getElementById('friend-modal-bg').classList.add('open');
            document.getElementById('friend-search-res').textContent = '';
            document.getElementById('friend-search-input').value = '';
        };

        window.closeAddFriendModal = () => document.getElementById('friend-modal-bg').classList.remove('open');

        window.submitFriendRequest = async () => {
            if(!auth.currentUser) return alert("Login required");
            const targetName = document.getElementById('friend-search-input').value.trim().toLowerCase();
            const resEl = document.getElementById('friend-search-res');
            if(!targetName) return;
            
            resEl.style.display = 'block';
            resEl.style.color = '#FFD700';
            resEl.textContent = 'Searching...';

            try {
                const snap = await get(child(ref(db), `users_by_name/${targetName}`));
                if(snap.exists()){
                    const target = snap.val();
                    if(target.uid === auth.currentUser.uid) { resEl.textContent="Can't add yourself!"; resEl.style.color='red'; return; }
                    
                    await set(ref(db, `friends/${auth.currentUser.uid}/${target.uid}`), { name: target.name, avatar: target.avatar || '', timestamp: Date.now() });
                    await set(ref(db, `friends/${target.uid}/${auth.currentUser.uid}`), { name: auth.currentUser.displayName || 'Friend', avatar: localStorage.getItem('cinephile_avatar') || '', timestamp: Date.now() });
                    
                    resEl.textContent = 'Connected with ' + target.name + '!';
                    resEl.style.color = '#a855f7';
                    setTimeout(()=>{ closeAddFriendModal(); loadFriends(); }, 1500);
                } else {
                    resEl.textContent = 'User not found.';
                    resEl.style.color = 'red';
                }
            } catch(e) { resEl.textContent = 'Error.'; }
        };

        window.loadFriends = async () => {
            if(!auth.currentUser) return;
            const snap = await get(child(ref(db), `friends/${auth.currentUser.uid}`));
            const list = document.getElementById('friend-list');
            list.innerHTML = '';
            if(snap.exists()){
                Object.values(snap.val()).sort((a,b)=>b.timestamp-a.timestamp).forEach(f=>{
                    const av = f.avatar ? `<img src="${f.avatar}">` : f.name.charAt(0).toUpperCase();
                    list.innerHTML += `
                        <div class="friend-item">
                            <div class="friend-avatar">${av}</div>
                            <span class="friend-name">${f.name}</span>
                        </div>
                    `;
                });
            } else {
                list.innerHTML = '<p style="color:#666; font-size:.8rem; margin-top:20px;">No friends added yet.</p>';
            }
        };

        // --- Local State ---
        let meName = localStorage.getItem('cinephile_user_name') || 'PLAYER';
        let currentAvatarUrl = localStorage.getItem('cinephile_avatar') || '';

        window.getLoadName = () => {
            meName = localStorage.getItem('cinephile_user_name') || 'PLAYER';
            currentAvatarUrl = localStorage.getItem('cinephile_avatar') || '';
            if(document.getElementById('nav-username')) document.getElementById('nav-username').textContent = meName;
            if(document.getElementById('profile-name-input')) document.getElementById('profile-name-input').value = meName;
            
            const initials = meName.charAt(0).toUpperCase();
            if(document.getElementById('nav-initial')) {
                document.getElementById('nav-initial').innerHTML = currentAvatarUrl ? `<img src="${currentAvatarUrl}">` : initials;
            }
            if(document.getElementById('profile-avatar-lg')) {
                document.getElementById('profile-avatar-lg').innerHTML = currentAvatarUrl ? `<img src="${currentAvatarUrl}">` : initials;
            }
        };

        window.changeAvatar = () => {
            const url = prompt("Avatar Image URL:", currentAvatarUrl);
            if(url !== null) {
                localStorage.setItem('cinephile_avatar', url.trim());
                const btn = document.getElementById('btn-save-profile');
                if(btn) btn.classList.remove('hidden');
                getLoadName();
            }
        };

        window.saveProfile = async () => {
            const newName = document.getElementById('profile-name-input').value.trim();
            if(!newName) return;
            localStorage.setItem('cinephile_user_name', newName);
            await fbUpdateProfile(newName, localStorage.getItem('cinephile_avatar') || '');
            getLoadName();
            const btn = document.getElementById('btn-save-profile');
            if(btn) btn.classList.add('hidden');
            toggleProfile();
        };

        document.addEventListener('DOMContentLoaded', () => {
            getLoadName();
            const inp = document.getElementById('profile-name-input');
            if(inp) inp.addEventListener('input', () => {
                const btn = document.getElementById('btn-save-profile');
                if(btn) btn.classList.toggle('hidden', inp.value.trim() === meName);
            });
        });
    </script>
"""

HTML_BLOCKS = """
    <!-- Panels Overlay -->
    <div class="panel-overlay" id="panel-overlay" onclick="closeAllPanels()"></div>

    <!-- Friends Panel -->
    <div class="friend-panel" id="friend-panel">
        <div class="panel-hdr">
            <h2>CONNECTIONS</h2>
            <button class="panel-close-btn" onclick="toggleFriendsPanel()"><i class='bx bx-x'></i></button>
        </div>
        <div class="friend-list" id="friend-list"></div>
        <div style="padding:30px;">
            <button class="friend-add-btn" onclick="openAddFriendModal()"><i class='bx bx-user-plus'></i> ADD NEW</button>
        </div>
    </div>

    <!-- Profile Panel -->
    <div class="profile-panel" id="profile-panel">
        <div class="panel-hdr">
            <h2>MY PROFILE</h2>
            <button class="panel-close-btn" onclick="toggleProfile()"><i class='bx bx-x'></i></button>
        </div>
        <div class="profile-body">
            <div style="position:relative;">
                <div class="profile-avatar-lg" id="profile-avatar-lg">?</div>
                <button onclick="changeAvatar()" style="position:absolute; bottom:0; right:0; background:#FFD700; border:none; width:34px; height:34px; border-radius:50%; cursor:pointer; display:flex; align-items:center; justify-content:center; box-shadow:0 0 10px rgba(0,0,0,.5);"><i class='bx bxs-camera'></i></button>
            </div>
            <div class="profile-input-group">
                <label>Experience Name</label>
                <input type="text" id="profile-name-input" class="profile-input">
            </div>
            <button id="btn-save-profile" class="save-btn hidden" onclick="saveProfile()"><i class='bx bx-save'></i> SAVE CHANGES</button>
        </div>
        <div style="padding:30px;">
            <button class="logout-btn" onclick="logout()"><i class='bx bx-log-out-circle'></i> DISCONNECT</button>
        </div>
    </div>

    <!-- Add Friend Modal -->
    <div class="modal-bg" id="friend-modal-bg">
        <div class="friend-modal">
            <button onclick="closeAddFriendModal()" style="position:absolute; top:20px; right:20px; background:none; border:none; color:#666; font-size:1.5rem; cursor:pointer;"><i class='bx bx-x'></i></button>
            <h3>CONNECT</h3>
            <p style="color:#888; font-size:.85rem; margin-bottom:25px;">Enter their exact Character Name to sync signals.</p>
            <input type="text" id="friend-search-input" class="profile-input" placeholder="e.g. Neo" style="margin-bottom:20px; border-color:rgba(168,85,247,.3);">
            <button class="friend-submit" onclick="submitFriendRequest()">ESTABLISH LINK</button>
            <p id="friend-search-res" style="margin-top:20px; font-weight:600; display:none;"></p>
        </div>
    </div>
"""

NAV_RIGHT_HTML = """
        <div class="nav-right" style="display:flex; flex-direction:column; align-items:flex-end; gap:8px;">
            <div style="display:flex; align-items:center; gap:12px;">
                <div class="friend-nav-btn" onclick="toggleFriendsPanel()" style="padding:6px; border-radius:50%; width:32px; height:32px; justify-content:center; border-color:rgba(168,85,247,.4); background:rgba(255,255,255,0.05); border:1px solid rgba(168,85,247,0.3); display:flex; align-items:center;">
                    <i class='bx bx-group' style="color:#a855f7; font-size:1.2rem;"></i>
                </div>
                <div class="profile-btn" onclick="toggleProfile()" style="padding:0; background:none; border:none;">
                    <div class="profile-avatar-sm" id="nav-initial" style="width:28px; height:28px; font-size:.9rem; border:1px solid rgba(255,215,0,.5); display:flex; align-items:center; justify-content:center; background:#FFD700; color:#000; border-radius:50%;">?</div>
                </div>
            </div>
            <span id="nav-username" class="profile-name-sm" style="font-size:.7rem; opacity:.6;">Welcome</span>
        </div>
"""

# PATCH DASHBOARD
if os.path.exists('03_dashboard.html'):
    with open('03_dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()
    if 'friend-panel' not in content:
        content = content.replace('</style>', FULL_PANEL_CSS + '\n</style>')
        content = content.replace('</body>', HTML_BLOCKS + '\n' + JS_MODULE_TEMPLATE + '\n</body>')
        content = content.replace('<div class="nav-spacer"></div>', NAV_RIGHT_HTML)
        with open('03_dashboard.html', 'w', encoding='utf-8') as f:
            f.write(content)

# PATCH ARCADE
if os.path.exists('06_arcade.html'):
    with open('06_arcade.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Clean previous profile UI in arcade
    content = re.sub(r'<!-- Profile Panel -->.*?<div class="profile-overlay".*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="profile-panel".*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="profile-overlay".*?</div>', '', content, flags=re.DOTALL)

    if 'friend-panel' not in content:
        content = content.replace('</style>', FULL_PANEL_CSS + '\n</style>')
        content = content.replace('</body>', HTML_BLOCKS + '\n' + JS_MODULE_TEMPLATE + '\n</body>')
        
        new_nav_arcade = """
        <div style="width:140px; display:flex; justify-content:flex-end; align-items:center; gap:12px;">
             <div class="friend-nav-btn" onclick="toggleFriendsPanel()" style="padding:6px; border-radius:50%; width:30px; height:30px; justify-content:center; background:rgba(255,255,255,0.05); border:1px solid rgba(168,85,247,0.3); display:flex; align-items:center;">
                <i class='bx bx-group' style="color:#a855f7; font-size:1.1rem;"></i>
            </div>
            <div class="profile-btn" onclick="toggleProfile()" style="padding:0; background:none; border:none;">
                <div class="profile-avatar-sm" id="nav-initial" style="width:28px; height:28px; font-size:.9rem; border:1px solid rgba(255,215,0,.5); display:flex; align-items:center; justify-content:center; background:#FFD700; color:#000; border-radius:50%;">?</div>
            </div>
        </div>
"""
        content = re.sub(r'<div style="width:140px; display:flex; justify-content:flex-end;">.*?</div>', new_nav_arcade, content, flags=re.DOTALL)
        
        with open('06_arcade.html', 'w', encoding='utf-8') as f:
            f.write(content)

print("Sync Complete.")
