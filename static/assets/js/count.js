let av=document.getElementById('price').value;
let cv=parseFloat(av);
let bv=document.getElementById('q').value;
let dv=parseFloat(bv);
let ev=cv*dv;
document.getElementById('stotal').innerHTML=ev;
