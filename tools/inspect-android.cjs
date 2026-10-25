const{chromium}=require('/opt/codex/cua_node/lib/node_modules/playwright');
(async()=>{const b=await chromium.connectOverCDP('http://127.0.0.1:9222');const p=b.contexts()[0].pages()[0];console.log(await p.evaluate(()=>({url:location.href,ready:document.readyState,title:document.title,html:document.documentElement.outerHTML.slice(0,3000)})));await b.close()})()
