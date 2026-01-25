let names = ['ashraf','mohsen','ahmed','oraby','zakariia'];
let ages  = ['20 years old','24 years old','28 years old','29 years old','31 years old'];

function all_card(name, age) {
  let card = document.createElement('div');
  let img = document.createElement('img');
  let p = document.createElement('p');
  let h3 = document.createElement('h3');

  h3.textContent = name;
  p.textContent = age;

  img.src = 'img/ashraf.png';
  img.style.width = '100px';

  card.appendChild(img);
  card.appendChild(h3);
  card.appendChild(p);

  card.style.background = '#666';
  card.style.color = '#fff';
  card.style.padding = '10px';
  card.style.textAlign = 'center';
  card.style.margin = '10px';
  card.style.display = 'inline-block';

  document.body.appendChild(card);
}

// إنشاء كل الكروت
for (let i = 0; i < names.length; i++) {
  all_card(names[i], ages[i]);
}

// التعامل مع الزرار
let btn = document.getElementById('btn');

btn.addEventListener('click', function () {
  document.body.style.background = 'blue';
  btn.style.color = 'red';
  btn.style.background = 'orange';
});
let btn2 = document.getElementById('btn2');
btn2.onmouseover=function () {
  document.body.style.background = 'red';
}
let dollar=document.getElementById(`dollar`)
let pound=document.getElementById(`pound`)
dollar.onkeyup=function(){
    pound.value=dollar.value*40

}
pound.onkeyup=function(){
    dollar.value=pound.value/40

}
let afterBtn = document.getElementById('afterBtn');
let beforeBtn = document.getElementById('beforeBtn');
let appendBtn = document.getElementById('appendBtn');
let content = document.getElementById('content');
let container = document.getElementById('container');

container.style.background = '#ffa';
container.style.height = '50px';
afterBtn.onclick=function(){
  container.after(content)
}
beforeBtn.onclick=function(){
  container.before(content)
}
appendBtn.onclick=function(){
      container.append(content)
}
let hello=document.getElementById(`hello`)
// hello.onclick=function(){
//   hello.classList.add("name")
// }
hello.oncontextmenu=function(){
  hello.classList.remove("name")
}
hello.onclick=function(){
  hello.classList.toggle("name")
}

let btnopen=document.getElementById(`open`)
let btnclose=document.getElementById(`close`)
let btnnavebar=document.getElementById(`nav`)
btnclose.onclick=function(){
  btnnavebar.classList.add(`hide`)
  this.classList.add(`hide`)
  btnopen.classList.remove('hide')
}
btnopen.onclick=function(){
  this.classList.add(`hide`)
  btnclose.classList.remove(`hide`)
  btnnavebar.classList.remove(`hide`)
}
input_test1=document.getElementById(`input_test1`)
button_test1=document.getElementById(`button_test1`)
button_test1.onclick=function(){
  button_test1.style.background=`red`
}
window.onload=function(){
  input_test1.focus()
}
input_test1.oncontextmenu=function(){
  input_test1.blur()
}
let button2 = document.getElementById('button2');

window.onscroll = function () {
  if (window.scrollY >= 400) {
    button2.style.display = 'block';
  } else {
    button2.style.display = 'none';
  }
};
button2.onclick=function(){
  window.scroll({
    left:0,
    top:0,
    behavior:"smooth"
  })
}
console.log(window.screen.width)
console.log(window.screen.height)
console.log(window.screen.availWidth)
console.log(window.screen.availHeight)
console.log(window.screen.colorDepth)
console.log(window.screen.pixelDepth)
console.log(window.screen.orientation.type)

console.log(window.location.href);      // العنوان كامل
console.log(window.location.origin);    // البروتوكول + الدومين
console.log(window.location.protocol);  // http: أو https:
console.log(window.location.host);      // الدومين + البورت
console.log(window.location.hostname);  // الدومين فقط
console.log(window.location.port);      // رقم البورت
console.log(window.location.pathname);  // اسم الصفحة
console.log(window.location.search);    // Query String
console.log(window.location.hash);      // #hash

// location.reload();                      // إعادة تحميل الصفحة
// location.href = "https://google.com";  // انتقال عادي
// location.assign("https://google.com"); // انتقال عادي
// location.replace("https://google.com");// انتقال بدون رجوع
// location.hash = "#section1";           // الانتقال داخل الصفحة
setTimeout(function(){
  console.log(`hellooooooo`)
},2000)
// clearTimeout()
i=0
rebeat=setInterval(function(){
console.log(i++)
if(i==4){
  clearInterval(rebeat)
}
},2000)

// if(localStorage.length>0){
// document.body.style.background=localStorage.getItem(`color`)
// }
// function setColor(color){
//   localStorage.setItem(`color`,color)
//   document.body.style.background=color
// }

if(localStorage.length>0){
document.body.style.background=sessionStorage.getItem(`color`)
}
function setColor(color){
  sessionStorage.setItem(`color`,color)
  document.body.style.background=color
}
