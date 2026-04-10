import os
import re

FILES_TO_PATCH = ['04_movies.html', '05_series.html'] # Will do Arcade separately if needed, since Arcade has custom socket logic

CSS_FRIENDS = """
        /* Friends UI */
        .friend-btn { display:flex; align-items:center; gap:8px; cursor:pointer; background:rgba(255,255,255,.05); padding:6px 12px; border-radius:30px; border:1px solid rgba(168,85,247,.3); transition:all .3s ease; color:var(--text); font-family:'Roboto Condensed'; font-size:.8rem; letter-spacing:1px; text-transform:uppercase; margin-bottom:8px; }
        .friend-btn:hover { background:rgba(168,85,247,.15); border-color:#a855f7; color:#fff; }
        
        .friend-panel { position:fixed; top:0; left:-400px; width:400px; height:100dvh; background:var(--surface); z-index:2000; transition:left .4s cubic-bezier(.25,1,.5,1); display:flex; flex-direction:column; box-shadow:10px 0 30px rgba(0,0,0,.5); }
        .friend-panel.open { left:0; }
        
        .friend-hdr { padding:30px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,.05); }
        .friend-hdr h2 { font-family:'Bebas Neue'; font-size:2rem; letter-spacing:4px; margin:0; }
        .friend-hdr button { background:none; border:none; color:var(--text-dim); font-size:1.8rem; cursor:pointer; transition:color .3s; }
        .friend-hdr button:hover { color:#e50914; }

        .friend-list { padding:20px 30px; flex:1; overflow-y:auto; display:flex; flex-direction:column; gap:15px; }
        
        .friend-item { display:flex; align-items:center; gap:15px; padding:10px; background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.05); border-radius:4px; transition:all .3s; }
        .friend-item:hover { border-color:rgba(168,85,247,.4); transform:translateY(-2px); }
        .friend-avatar { width:45px; height:45px; border-radius:50%; background:#a855f7; display:flex; align-items:center; justify-content:center; color:#fff; font-family:'Bebas Neue'; font-size:1.5rem; overflow:hidden;}
        .friend-avatar img { width:100%; height:100%; object-fit:cover; }
        .friend-info { display:flex; flex-direction:column; flex:1; overflow:hidden;}
        .friend-name { font-family:'Poppins'; font-size:.95rem; font-weight:600; color:#fff; white-space:nowrap; text-overflow:ellipsis; overflow:hidden;}

        .friend-actions { padding:20px 30px; border-top:1px solid rgba(255,255,255,.05); }
        .friend-add-btn { width:100%; display:flex; justify-content:center; align-items:center; gap:8px; padding:12px; background:var(--surface2); border:1px solid #a855f7; color:#a855f7; font-family:'Roboto Condensed'; font-size:.9rem; letter-spacing:1px; cursor:pointer; border-radius:4px; transition:all .3s; }
        .friend-add-btn:hover { background:rgba(168,85,247,.1); color:#fff; }

        .friend-modal-bg { position:fixed; inset:0; background:rgba(0,0,0,.8); z-index:3000; display:none; align-items:center; justify-content:center; backdrop-filter:blur(5px); }
        .friend-modal-bg.open { display:flex; }
        .friend-modal { background:var(--surface); width:90%; max-width:400px; padding:30px; border-radius:8px; border:1px solid rgba(168,85,247,.3); box-shadow:0 10px 40px rgba(0,0,0,.5); text-align:center; position:relative;}
        .friend-modal h3 { font-family:'Bebas Neue'; font-size:2.2rem; letter-spacing:2px; margin-bottom:15px; color:#fff; }
        .friend-modal p { font-family:'Poppins'; font-size:.8rem; color:var(--text-dim); margin-bottom:20px; }
        .friend-input { width:100%; background:var(--surface2); border:1px solid rgba(255,255,255,.1); padding:12px 15px; border-radius:4px; color:#fff; font-family:'Poppins'; font-size:1rem; outline:none; transition:all .3s; margin-bottom:20px; }
        .friend-input:focus { border-color:#a855f7; }
        .friend-submit { width:100%; padding:12px; background:#a855f7; border:none; color:#fff; font-family:'Roboto Condensed'; font-size:1rem; letter-spacing:1px; border-radius:4px; cursor:pointer; transition:transform .3s; font-weight:700;}
        .friend-submit:hover { transform:translateY(-2px); box-shadow:0 5px 15px rgba(168,85,247,.4); }
"""

HTML_FRIENDS = """
    <!-- Friends System -->
    <div class="panel-overlay" id="friend-overlay" onclick="toggleFriendsPanel()"></div>
    <div class="friend-panel" id="friend-panel">
        <div class="friend-hdr">
            <h2>NETWORK</h2>
            <button onclick="toggleFriendsPanel()"><i class='bx bx-x'></i></button>
        </div>
        <div class="friend-list" id="friend-list">
            <!-- Friend items inject here -->
        </div>
        <div class="friend-actions">
            <button class="friend-add-btn" onclick="openAddFriendModal()"><i class='bx bx-user-plus'></i> ADD CONNECTION</button>
        </div>
    </div>

    <div class="friend-modal-bg" id="friend-modal-bg">
        <div class="friend-modal">
            <button onclick="closeAddFriendModal()" style="position:absolute; top:15px; right:15px; background:none; border:none; color:var(--text-dim); font-size:1.5rem; cursor:pointer;"><i class='bx bx-x'></i></button>
            <h3>ADD A LISTENER</h3>
            <p>Enter the exact Character Name of the person you want to connect with.</p>
            <input type="text" id="friend-search-input" class="friend-input" placeholder="e.g. JohnWick99">
            <button class="friend-submit" onclick="submitFriendRequest()">SEND PING</button>
            <p id="friend-search-res" style="margin-top:15px; font-size:.85rem; font-weight:600; display:none;"></p>
        </div>
    </div>
"""

JS_FRIENDS = """
        // --- FRIENDS LOGIC ---
        import { get, child } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-database.js";

        window.toggleFriendsPanel = () => {
            document.getElementById('friend-panel').classList.toggle('open');
            document.getElementById('friend-overlay').classList.toggle('open');
            if(document.getElementById('friend-panel').classList.contains('open')) loadFriends();
        };

        window.openAddFriendModal = () => {
            document.getElementById('friend-modal-bg').classList.add('open');
            document.getElementById('friend-search-res').style.display = 'none';
            document.getElementById('friend-search-input').value = '';
        };

        window.closeAddFriendModal = () => {
            document.getElementById('friend-modal-bg').classList.remove('open');
        };

        window.submitFriendRequest = async () => {
            if(!auth || !auth.currentUser) return alert("Please log in again to add friends!");
            const targetName = document.getElementById('friend-search-input').value.trim().toLowerCase();
            const resEl = document.getElementById('friend-search-res');
            resEl.style.display = 'block';
            
            if(!targetName) { resEl.textContent = "Please enter a name."; resEl.style.color = "var(--danger)"; return; }
            if(targetName === (auth.currentUser.displayName || '').toLowerCase()) {
                resEl.textContent = "You can't add yourself!"; resEl.style.color = "var(--danger)"; return; 
            }

            resEl.textContent = "Searching Database...";
            resEl.style.color = "var(--gold)";

            try {
                const snapshot = await get(child(ref(db), `users_by_name/${targetName}`));
                if (snapshot.exists()) {
                    const targetData = snapshot.val();
                    const targetUid = targetData.uid;
                    const myUid = auth.currentUser.uid;
                    
                    // Create reciprocal friend link
                    await set(ref(db, `friends/${myUid}/${targetUid}`), { name: targetData.name, avatar: targetData.avatar || '', timestamp: Date.now() });
                    // Also let's give the other friend our info (optional but polite)
                    await set(ref(db, `friends/${targetUid}/${myUid}`), { name: auth.currentUser.displayName, avatar: localStorage.getItem('cinephile_avatar') || '', timestamp: Date.now() });
                    
                    resEl.textContent = `Connection Established with ${targetData.name}!`;
                    resEl.style.color = "#a855f7"; // Neon Purple success
                    
                    setTimeout(() => {
                        closeAddFriendModal();
                        loadFriends();
                    }, 1500);
                } else {
                    resEl.textContent = "Signal lost. No Character found with that exact name.";
                    resEl.style.color = "var(--danger)";
                }
            } catch (e) {
                console.error(e);
                resEl.textContent = "Database Error. Try again.";
                resEl.style.color = "var(--danger)";
            }
        };

        window.loadFriends = async () => {
            if(!auth || !auth.currentUser) return;
            const uid = auth.currentUser.uid;
            
            try {
                const snapshot = await get(child(ref(db), `friends/${uid}`));
                const listEl = document.getElementById('friend-list');
                listEl.innerHTML = '';
                
                if (snapshot.exists()) {
                    const friends = snapshot.val();
                    const arr = Object.values(friends).sort((a,b)=>b.timestamp - a.timestamp);
                    arr.forEach(f => {
                        const av = f.avatar ? `<img src="${f.avatar}">` : f.name.charAt(0).toUpperCase();
                        listEl.innerHTML += `
                            <div class="friend-item">
                                <div class="friend-avatar">${av}</div>
                                <div class="friend-info">
                                    <span class="friend-name">${f.name}</span>
                                </div>
                                <button style="background:none; border:none; color:var(--text-dim); cursor:pointer;" onclick="alert('Viewing watchlists coming soon!')">
                                    <i class='bx bx-dots-vertical-rounded'></i>
                                </button>
                            </div>
                        `;
                    });
                } else {
                    listEl.innerHTML = `<p style="color:var(--text-dim); font-size:.85rem; text-align:center; margin-top:20px;">No connections established yet.</p>`;
                }
            } catch(e) { console.error("Error loading friends", e); }
        };
"""

for fname in FILES_TO_PATCH:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Inject CSS
    if 'friend-modal' not in content:
        content = content.replace('</style>', CSS_FRIENDS + '\n</style>')
    
    # 2. Inject HTML
    if 'friend-panel' not in content:
        content = content.replace('<!-- Profile Overlay & Panel -->', HTML_FRIENDS + '\n    <!-- Profile Overlay & Panel -->')
    
    # 3. Inject JS
    if 'loadFriends' not in content:
        # Find the script type="module" block end and inject before closing
        content = content.replace('</script>\n</body>', JS_FRIENDS + '\n</script>\n</body>')
    
    # 4. Bind the Nav Buttons!
    # Original: <button class="friends-btn" onclick="alert('Friends list coming soon!')">
    btn1 = """<button class="friends-btn" onclick="alert('Friends list coming soon!')">"""
    btn1_new = """<button class="friends-btn" onclick="toggleFriendsPanel()">"""
    content = content.replace(btn1, btn1_new)
    
    btn2 = """<button class="friends-btn" onclick="alert('Add Friends coming soon!')">"""
    btn2_new = """<button class="friends-btn" onclick="openAddFriendModal()">"""
    content = content.replace(btn2, btn2_new)

    # Note: the nav buttons in 04_movies and 05_series are in `.friends-row`
    
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)

print("Friends Module Patched Successfully!")
