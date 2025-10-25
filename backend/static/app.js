let sessionId = null;
let targetId = null;

const el = (id)=>document.getElementById(id);

el('btnStart').onclick = async ()=>{
  const r = await fetch('/sessions/start', {method:'POST'});
  const data = await r.json();
  sessionId = data.session_id;
  targetId = data.target_id;
  el('sessionInfo').innerText = `Session: ${sessionId}\nTarget ID: ${targetId}\nMonitor: ${data.opening_prompt}`;
  el('monitorOut').innerText = data.opening_prompt;
};

el('btnSend').onclick = async ()=>{
  if(!sessionId) return alert('Start a session first.');
  const stage = el('stage').value;
  const viewer_text = el('viewerInput').value;
  el('viewerInput').value='';
  const r = await fetch('/sessions/log', {method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({session_id: sessionId, stage, viewer_text})
  });
  const data = await r.json();
  el('monitorOut').innerText = data.monitor_prompt;
};

el('btnAdvance').onclick = async ()=>{
  if(!sessionId) return alert('Start a session first.');
  const to_stage = el('stage').value;
  const r = await fetch('/sessions/advance', {method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({session_id: sessionId, to_stage})
  });
  const data = await r.json();
  el('monitorOut').innerText = data.monitor_prompt;
};

el('btnFinish').onclick = async ()=>{
  if(!sessionId) return alert('Start a session first.');
  await fetch('/sessions/finish', {method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({session_id: sessionId})
  });
  alert('Session finished. You can run judging now.');
};

el('btnJudge').onclick = async ()=>{
  if(!sessionId) return alert('Start a session first.');
  const r = await fetch('/judging/run', {method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({session_id: sessionId, n_candidates: 5, use_clip: false})
  });
  const data = await r.json();
  const lines = data.ranking.map(x=>`Rank ${x.rank}: ${x.candidate_path}`).join('\n');
  el('judgingOut').innerText = `Effect size: ${data.effect_size.toFixed(3)} | Avg rank: ${data.average_rank.toFixed(2)}\n` + lines;
};
