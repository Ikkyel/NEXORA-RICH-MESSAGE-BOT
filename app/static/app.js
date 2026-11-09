/* ============================================
PROJECT : NEXORA RICH MESSAGE BOT
FILE    : app/static/app.js
FUNGSI  : Interaksi Mini App dan pemanggilan API
============================================ */
const tg=window.Telegram?.WebApp;tg?.ready();tg?.expand();
const initData=tg?.initData||'';const user=tg?.initDataUnsafe?.user;
document.getElementById("who").textContent = `WebApp: ${tg ? "tersedia" : "tidak ada"} | initData: ${initData ? "ada" : "kosong"} | platform: ${tg?.platform || "-"}`;
const headers={'Content-Type':'application/json','X-Telegram-Init-Data':initData};
async function api(path,opts={}){const r=await fetch(path,{...opts,headers:{...headers,...opts.headers}});const data=await r.json();if(!r.ok)throw new Error(data.detail||'Permintaan gagal');return data}
function notice(s){document.getElementById('notice').textContent=s}
async function load(){try{const [ds,dr,hs]=await Promise.all([api('/api/destinations'),api('/api/drafts'),api('/api/history')]);const sel=document.getElementById('destination');sel.innerHTML='<option value="">Pilih tujuan</option>'+ds.map(d=>`<option value="${d.id}">${esc(d.title)}</option>`).join('');document.getElementById('drafts').innerHTML=dr.map(d=>`<div class="item"><b>${esc(d.title)}</b><br><small>${esc(d.status)} · ${esc((d.text||'').slice(0,100))}</small><button class="small" onclick="sendDraft(${d.id})">Posting</button></div>`).join('')||'Belum ada draft.';document.getElementById('history').innerHTML=hs.map(h=>`<div class="item"><b>${esc(h.destination||'Tujuan')}</b><br><small>${esc(h.status)} · ${esc(h.detail||'')} · ${esc(h.created_at||'')}</small></div>`).join('')||'Belum ada riwayat.'}catch(e){notice(e.message)}}
function esc(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function payload(){const dt=document.getElementById('scheduled').value;return {title:document.getElementById('title').value||'Draft',text:document.getElementById('message').value,media_type:document.getElementById('mediaType').value||null,media_file_id:document.getElementById('fileId').value||null,destination_id:Number(document.getElementById('destination').value)||null,scheduled_at:dt?new Date(dt).toISOString():null,parse_mode:'HTML',buttons:document.getElementById('buttons').value.trim()?JSON.parse(document.getElementById('buttons').value):[]}}
document.getElementById('save').onclick=async()=>{try{const p=payload();if(p.scheduled_at)p.status='scheduled';await api('/api/drafts',{method:'POST',body:JSON.stringify(p)});notice('Draft berhasil disimpan.');await load()}catch(e){notice(e.message)}};
document.getElementById('publish').onclick=async()=>{try{const p=payload();const d=await api('/api/drafts',{method:'POST',body:JSON.stringify(p)});await sendDraft(d.id)}catch(e){notice(e.message)}};
window.sendDraft=async id=>{try{await api(`/api/drafts/${id}/publish`,{method:'POST'});notice('Posting berhasil dikirim.');await load()}catch(e){notice(e.message)}};
document.getElementById('refresh').onclick=load;
document.getElementById('addDest').onclick=async()=>{
    const title=document.getElementById('destTitle').value.trim();
    const chatId=document.getElementById('destChat').value.trim();

    if(!title || !chatId){
        notice('Nama channel dan Chat ID wajib diisi.');
        return;
    }

    if(!/^-?\d+$/.test(chatId)){
        notice('Chat ID harus berupa angka.');
        return;
    }

    try{
        notice('Sedang menambahkan tujuan...');
        await api('/api/destinations',{
            method:'POST',
            body:JSON.stringify({
                title,
                chat_id:Number(chatId),
                chat_type:'channel'
            })
        });
        notice('Tujuan berhasil ditambahkan.');
        await load();
    }catch(e){
        notice('Gagal menambahkan tujuan: '+e.message);
    }
};
if(initData)load();else notice('Mini App harus dibuka dari tombol bot Telegram.');
