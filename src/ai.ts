export function aiFailure(reason?:string){
 if(reason==='unconfigured')return 'Gemini is not configured for this server.';
 if(reason==='configuration_error')return 'The Gemini connection needs attention.';
 if(reason==='authentication_error')return 'Gemini access could not be authorised.';
 if(reason==='rate_limited')return 'Gemini is busy. Please try again later.';
 if(reason==='timeout')return 'Gemini took too long to respond.';
 if(reason==='invalid_response')return 'The AI response did not pass our checks.';
 return 'Gemini is temporarily unavailable.';
}
export async function aiRequest(url:string,body:unknown,signal:AbortSignal){
 const response=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body),signal});
 if(!response.ok)throw Error(response.status===429?'rate_limited':'unavailable');
 return response.json();
}
