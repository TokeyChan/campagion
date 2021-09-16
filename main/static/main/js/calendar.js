(()=>{"use strict";function e(e,t,n,i=null){for(;e.firstChild;)e.removeChild(e.firstChild);let a=null,o=new Date(t.get_time().getFullYear(),t.get_time().getMonth(),1).getDay()-1,s=new Date(t.get_time().getFullYear(),t.get_time().getMonth()+1,0).getDate();for(let t=0;t<o;t++){const t=document.createElement("div");Object.assign(t.style,{width:"40px",height:"34px",margin:"0 1px"}),e.appendChild(t)}for(let o=0;o<s;o++){const s=document.createElement("div"),l=new Date(t.get_time().getFullYear(),t.get_time().getMonth(),1+o);s.date=l,s.textContent=s.date.getDate(),Object.assign(s.style,{textAlign:"center",width:"40px",height:"40px",lineHeight:"40px",borderRadius:"50%",margin:"0 1px"}),s.addEventListener("mouseenter",(()=>{a!==s&&(s.style.backgroundColor="#1ab5e0",s.style.color="#FFFFFF")})),s.addEventListener("mouseleave",(()=>{a!==s&&(s.style.backgroundColor="",s.style.color="#000000")})),s.addEventListener("click",(e=>{var t;null!==a&&Object.assign(a.style,{backgroundColor:"",color:""}),Object.assign(s.style,{backgroundColor:"#286495",color:"#FFF"}),a=s,1!=e.detail.custom&&(n.value=`${(t=e.target.date).getDate()}/${t.getMonth()+1}/${t.getFullYear()}`,n.dispatchEvent(new CustomEvent("date_chosen")))})),null!=i&&i.getTime()==l.getTime()&&s.dispatchEvent(new CustomEvent("click",{detail:{custom:!0}})),e.appendChild(s)}}const t=["Mo","Di","Mi","Do","Fr","Sa","So"],n=["Jänner","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"];function i(e,t,n,i,o,s){const l=document.createElement("button");return Object.assign(l.style,{backgroundColor:"transparent",border:"none",fontSize:"20px",transform:"scale(1,1)",height:"60px",lineHeight:"60px",color:"#FFFFFF"}),l.addEventListener("mouseover",(()=>{l.style.cursor="pointer"})),l.addEventListener("click",(()=>{e.set_time(new Date(e.get_time().getFullYear(),e.get_time().getMonth()+n)),a(i,o,e,s)})),1==n&&s.addEventListener("input",(()=>{const t=s.value.split("/"),n=e.get_time();var l=[n.getDate(),n.getMonth(),n.getFullYear()];for(let e=0;e<t.length;e++){var r=parseInt(t[e]);isNaN(r)||(l[e]=r),2==e&&4===t[2].length&&s.dispatchEvent(new CustomEvent("date_chosen"))}e.set_time(new Date(l[2],l[1]-1)),a(i,o,e,s,new Date(l[2],l[1]-1,l[0]))})),l.textContent=t,l}function a(t,i,a,o,s=null){e(i,a,o,s),t.textContent=n[a.get_time().getMonth()]+" "+a.get_time().getFullYear()}function o(){this.time=new Date,this.get_time=function(){return this.time},this.set_time=function(e){this.time=e}}class s extends HTMLElement{constructor(){super(),this.input=document.createElement("input"),this.input.type="text",this.attachShadow({mode:"open"});const e=document.createElement("style");e.textContent=":host { all: initial }",this.shadowRoot.appendChild(e)}connectedCallback(){var a,s;this._value=this.attributes.value?.value??null,this.shadowRoot.appendChild(this.input),this.container=function(a){const s=new o,[l,r,d,c]=function(e){const t=document.createElement("div"),n=document.createElement("div"),i=document.createElement("div"),a=document.createElement("div");return Object.assign(n.style,{width:"294px",textAlign:"center",display:"flex",justifyContent:"space-between",height:"60px",padding:"0 20px",backgroundColor:"#1ab5e0"}),Object.assign(a.style,{width:"294px",display:"flex",flexWrap:"wrap",margin:"0 20px 20px 20px"}),Object.assign(i.style,{width:"294px",display:"flex",flexWrap:"wrap",padding:"0px 20px 0px 20px"}),Object.assign(t.style,{width:"334px",display:"none",fontFamily:'Calibri, "Trebuchet MS", Candara, Segoe, "Segoe UI", Optima, Arial, sans-serif',boxShadow:"1px 3px 10px rgba(0, 0, 0, 0.2)",position:"absolute",zIndex:"3",backgroundColor:"white"}),t.addEventListener("click",(e=>e.stopPropagation())),t.appendChild(n),t.appendChild(i),t.appendChild(a),e.appendChild(t),[t,n,i,a]}(a.parentNode);return function(e,t,a,o){const s=document.createElement("div");Object.assign(s.style,{width:"150px",display:"inline-block",fontWeight:"bold",marginBottom:"5px",height:"60px",lineHeight:"60px",color:"#FFFFFF"}),s.textContent=n[a.get_time().getMonth()]+" "+a.get_time().getFullYear();const l=i(a,"<",-1,s,t,o),r=i(a,">",1,s,t,o);e.append(l,s,r)}(r,c,s,a),function(e){for(let n=0;n<7;n++){const i=document.createElement("div");i.textContent=t[n],Object.assign(i.style,{textAlign:"center",width:"42px",height:"40px",lineHeight:"40px",fontWeight:"bold"}),e.appendChild(i)}}(d),e(c,s,a),l}(this.input),a=this.input,s=this.container,a.addEventListener("focus",(()=>{a.dispatchEvent(new CustomEvent("change")),s.style.display="block"})),((e,t)=>{window.addEventListener("click",(()=>{t.style.display="none"})),e.addEventListener("click",(e=>{e.stopPropagation()}))})(this.input,this.container),this.input.addEventListener("date_chosen",(()=>{this._value=this.input.value,this.dispatchEvent(new CustomEvent("change"))})),this.input.value=this._value}get value(){return this._value}set value(e){this.setAttribute("value",e),this._value=e,this.input.value=e,this.dispatchEvent(new CustomEvent("change"))}}customElements.define("carbox-picker",s)})();