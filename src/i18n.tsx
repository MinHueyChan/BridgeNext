import React,{createContext,useContext,useEffect,useState} from 'react';
import {dictionary} from './translations';
export type Locale='en'|'ms'|'zh';
const Context=createContext({locale:'en' as Locale,setLocale:(_v:Locale)=>{}});
export const usePreferences=()=>useContext(Context);
export function translate(text:string,locale:Locale):string{
 if(locale==='en')return text;
 const trim=text.trim(),pair=dictionary[trim];
 if(pair)return text.replace(trim,pair[locale==='ms'?0:1]);
 // Only controlled UI templates; never translate arbitrary fragments of user input.
 const sdg=trim.match(/^Develops (.+) as an employment-relevant vocational capability\.$/);
 if(sdg){const name=Object.keys(dictionary).find(key=>key.toLowerCase()===sdg[1]);const skill=name?translate(name,locale):sdg[1];return locale==='zh'?`发展与就业相关的${skill}职业能力。`:`Membangunkan ${skill} sebagai kemahiran pekerjaan yang relevan.`}
 const month=trim.match(/^([A-Z][a-z]+) (20\d{2})$/);
 if(month&&dictionary[month[1]])return `${dictionary[month[1]][locale==='ms'?0:1]} ${month[2]}`;
 const templates:[RegExp,string,string][]=[[/^(.+)'s synthetic profile is ready to explore\.$/,'Profil sintetik $1 sedia diterokai.','$1 的合成演示资料已准备好。'],[/^([\d.]+)% automation-pattern share$/,'$1% bahagian corak automasi','$1% 自动化模式占比'],[/^([\d.]+) hours$/,'$1 jam','$1 小时'],[/^([\d.]+) hrs$/,'$1 jam','$1 小时'],[/^([\d.]+) weeks$/,'$1 minggu','$1 周'],[/^WEEK (.+)$/,'MINGGU $1','第 $1 周'],[/^(\d+) years$/,'$1 tahun','$1 年'],[/^(\d+) hours$/,'$1 jam','$1 小时'],[/^After step (\d+) · build on the previous learning activity$/,'Selepas langkah $1 · teruskan aktiviti sebelumnya','完成第 $1 步后继续学习'],[/^Step (\d+) of 4$/,'Langkah $1 daripada 4','第 $1 步，共 4 步'],[/^Remove (.+)$/,'Buang $1','移除 $1'],[/^Choose (.+)$/,'Pilih $1','选择 $1']];
 for(const [pattern,ms,zh] of templates)if(pattern.test(trim))return trim.replace(pattern,locale==='ms'?ms:zh);
 return text;
}
/** Localize presentation elements before React renders, without mutating DOM or canonical data. */
export function localize(node:React.ReactNode,locale:Locale):React.ReactNode{
 if(typeof node==='string')return translate(node,locale);
 if(Array.isArray(node))return node.map(child=>localize(child,locale));
 if(!React.isValidElement(node))return node;
 const props=node.props as Record<string,any>;
 if(props.translate==='no')return node;
 const next:Record<string,any>={};
 for(const key of ['aria-label','placeholder','title'])if(typeof props[key]==='string')next[key]=translate(props[key],locale);
 if(node.type==='option'&&props.value===undefined&&typeof props.children==='string')next.value=props.children;
 if(props.children!==undefined)next.children=localize(props.children,locale);
 return React.cloneElement(node,next);
}
export function PreferencesProvider({children}:{children:React.ReactNode}){
 const[locale,setLocale]=useState<Locale>(()=>{const v=localStorage.getItem('bn-language');return v==='ms'||v==='zh'?v:'en'});
 useEffect(()=>{document.documentElement.lang=locale==='zh'?'zh-Hans':locale;localStorage.setItem('bn-language',locale)},[locale]);
 useEffect(()=>{localStorage.removeItem('bn-low-data');const link=document.createElement('link');link.rel='stylesheet';link.href='https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;450;500;550;600;650;700&family=Manrope:wght@400;500;600;650;700;750;800&display=swap';document.head.append(link);return()=>link.remove()},[]);
 return <Context.Provider value={{locale,setLocale}}>{children}</Context.Provider>;
}
export function LanguagePicker(){const {locale,setLocale}=usePreferences();return <div className="language-controls" translate="no"><select aria-label="Language / Bahasa / 语言" value={locale} onChange={e=>setLocale(e.target.value as Locale)}><option value="en">English</option><option value="ms">Bahasa Malaysia</option><option value="zh">中文</option></select></div>}
