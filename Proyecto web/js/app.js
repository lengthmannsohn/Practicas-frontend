// Carga y filtros básicos sin librerías
const stats = $('#stats');
const fBarrio = $('#fBarrio');
const fIdioma = $('#fIdioma');
const fHorario = $('#fHorario');
const fPrecioMax = $('#fPrecioMax');
const btnLimpiar = $('#btnLimpiar');

let DATA = [];
let BARRIOS = new Set();

async function init(){
const res = await fetch('./data/data.json');
DATA = await res.json();
DATA.forEach(x=>BARRIOS.add(x.barrio));
// Rellena select barrios
[...BARRIOS].sort().forEach(b=>{
const opt = document.createElement('option');
opt.value = b; opt.textContent = b; fBarrio.appendChild(opt);
});
render();
}

function filtrar(){
const barrio = fBarrio.value;
const idioma = fIdioma.value;
const horario = fHorario.value;
const precioMax = Number(fPrecioMax.value || 0);
return DATA.filter(p=>{
if (barrio && p.barrio !== barrio) return false;
if (idioma && !p.idiomas.includes(idioma)) return false;
if (horario && p.horario !== horario) return false;
if (precioMax && p.precio_desde > precioMax) return false;
return true;
});
}

function card(p){
return `
<article class="card">
<h3>${p.alias} ${p.verificado ? '✔️' : ''}</h3>
<p class="muted">${p.barrio} · desde ${p.precio_desde}€ · ${p.horario}</p>
<ul class="pillset">
${p.idiomas.map(i=>`<li class="pill">${i}</li>`).join('')}
</ul>
<a class="btn secondary" href="perfil.html?alias=${encodeURIComponent(p.alias)}">Ver perfil</a>
</article>`;
}

function render(){
const arr = filtrar();
stats.textContent = `${arr.length} resultados · Datos ficticios para pruebas internas`;
listado.innerHTML = arr.map(card).join('');
}

[fBarrio,fIdioma,fHorario,fPrecioMax].forEach(el=>el && el.addEventListener('input',render));
btnLimpiar && btnLimpiar.addEventListener('click', ()=>{
fBarrio.value = '';
fIdioma.value = '';
fHorario.value = '';
fPrecioMax.value = '';
render();
});

init();