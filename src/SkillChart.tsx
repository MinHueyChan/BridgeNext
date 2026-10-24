import {ResponsiveContainer,RadarChart,Radar,PolarGrid,PolarAngleAxis,PolarRadiusAxis,Tooltip} from 'recharts';
import {translate,usePreferences} from './i18n';
export interface SkillChartRow {subject:string;confidence:number|null}
type Point={x:number;y:number;value?:number|null;payload?:SkillChartRow};
export default function SkillChart({data}:{data:SkillChartRow[]}){
 const {locale}=usePreferences();const complete=data.every(row=>row.confidence!==null);
 const rows=data.map(row=>({...row,subject:translate(row.subject,locale)}));
 // Recharts places null radial values at the centre. A custom shape avoids
 // drawing those as zero or inventing a filled polygon through unrated groups.
 function confidenceShape({points=[]}:{points?:Point[]}){const rated=points.filter(point=>point.payload?.confidence!=null);return <g className="skill-confidence-shape">{complete&&<polygon className="skill-confidence-area" points={rated.map(point=>`${point.x},${point.y}`).join(' ')} stroke="#3d7156" strokeWidth={2} fill="#7aa78b" fillOpacity={.36}/>} {rated.map((point,index)=><circle className="skill-confidence-dot" key={index} cx={point.x} cy={point.y} r={4} fill="#3d7156" stroke="white" strokeWidth={1.5}><title>{point.payload?.subject}: {point.payload?.confidence}/5</title></circle>)}</g>}
 return <div className="skill-confidence-chart" role="img" aria-label={translate('Five-group self-assessed skill chart',locale)}><ResponsiveContainer><RadarChart data={rows} outerRadius="74%" margin={{top:12,right:28,bottom:12,left:28}}><PolarGrid gridType="polygon" stroke="#dce3d9"/><PolarAngleAxis dataKey="subject" tick={{fontSize:11,fill:'#6d776c'}}/><PolarRadiusAxis domain={[0,5]} ticks={[1,2,3,4,5]} tick={false} axisLine={false}/><Radar name={translate('Your self-rating:',locale)} dataKey="confidence" shape={confidenceShape} activeDot={false} isAnimationActive={false}/><Tooltip formatter={value=>[`${value}/5`,translate('Your self-rating:',locale)]}/></RadarChart></ResponsiveContainer></div>;
}
