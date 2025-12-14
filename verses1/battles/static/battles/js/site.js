
document.addEventListener('DOMContentLoaded', function(){
  
  const observer = new IntersectionObserver((entries)=>{
    entries.forEach(entry=>{
      if(entry.isIntersecting){
        entry.target.classList.add('visible');
      }
    });
  },{threshold:.15});
  document.querySelectorAll('.fade-in').forEach(el=>observer.observe(el));

  
  const nav = document.querySelector('.navbar');
  if(nav){
    const onScroll = ()=>{
      if(window.scrollY>30) nav.classList.add('scrolled'); else nav.classList.remove('scrolled');
    };
    window.addEventListener('scroll', onScroll);
    onScroll();
  }


  document.querySelectorAll('.copy-battle-code').forEach(btn=>{
    btn.addEventListener('click', async (e)=>{
      const code = btn.dataset.code;
      try{ await navigator.clipboard.writeText(code); btn.innerText='Copied'; setTimeout(()=>btn.innerText='Copy',2000);}catch(err){console.warn('copy failed',err);}
    });
  });

  
  if(typeof bootstrap!=='undefined'){
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el=>{
      new bootstrap.Tooltip(el);
    });
  }


  (function setupBattlePolling(){
    const statusEl = document.getElementById('battle-status');
    if(!statusEl) return;
    
    const match = window.location.pathname.match(/\/battle\/(\d+)\//);
    if(!match) return;
    const battleId = match[1];
    const statusUrl = `/battle/${battleId}/status/`;

    let lastOpponentJoined = false;
    let lastSubmissionsCount = 0;

    const poll = async ()=>{
      try{
        const res = await fetch(statusUrl, {credentials: 'same-origin'});
        if(!res.ok) return;
        const j = await res.json();
        
        if(!lastOpponentJoined && j.opponent_joined){
          window.location.reload();
          return;
        }
        lastOpponentJoined = j.opponent_joined;

        if(j.submissions_count !== lastSubmissionsCount && lastSubmissionsCount !== 0){
          window.location.reload();
          return;
        }
        lastSubmissionsCount = j.submissions_count;

        if(j.opponent_joined && !j.is_completed){
          statusEl.textContent = 'Opponent joined — you can submit your code.';
        }
        if(j.is_completed){
          window.location.href = j.result_url;
        }
      }catch(e){ console.warn('status poll failed', e); }
    };

    setInterval(poll, 2000);
    poll();
  })();
});
