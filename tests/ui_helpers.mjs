// User-input setup shared by browser checks; no seeded demo identity or completion.
export const button=(page,name)=>page.getByRole('button',{name,exact:true});
export const profile=page=>page.evaluate(()=>JSON.parse(sessionStorage.getItem('bn-profile')));
export async function nav(page,name){if(await button(page,'Open navigation').isVisible())await button(page,'Open navigation').click();const item=page.locator('.sidebar nav').getByRole('button',{name,exact:true});await item.focus();await item.press('Enter')}
export async function questionnaire(page,{custom,occupation}={}){
 await button(page,'Find my next direction').click();
 if(occupation)await button(page,`Choose ${occupation}`).click();
 if(custom){await button(page,'I do something else').click();await page.getByPlaceholder('e.g. Procurement assistant').fill(custom)}
 await page.getByLabel('Years of experience',{exact:true}).fill('7');await page.getByLabel('Weekly learning hours',{exact:true}).fill('6');
 await button(page,'Continue').click();await page.locator('.picker-item').filter({hasText:'Microsoft Excel'}).click();await button(page,'Continue').click();await page.locator('.rating-buttons button').nth(2).click();await button(page,'Continue').click();await button(page,'Finance').click();await button(page,'Confirm profile & see my top match').click();await page.getByRole('heading',{name:'A direction to start with.'}).waitFor();
}
export async function enter(page,destination='My profile'){await nav(page,destination);await page.getByRole('heading',{name:'Keep your next chapter with you.'}).waitFor();await button(page,'Log in').click()}
export async function exit(page){await page.locator('.avatar-button').click();await button(page,'Exit prototype').click();await page.locator('.guest-pill').filter({hasText:'Guest mode'}).waitFor()}
export async function complete(page){for(const item of await page.getByLabel('Mark complete',{exact:true}).all())await item.check()}
export async function collect(page){await button(page,'Complete pathway & collect badge').click();await page.getByLabel('What did you learn?',{exact:true}).fill('I practised checking generated summaries against original financial records.');await page.getByLabel('I confirm that I completed these learning activities.',{exact:true}).check();await button(page,'Collect my badge').click();await button(page,'View my achievements').click()}
