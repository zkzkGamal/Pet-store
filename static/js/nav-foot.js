
const createnav = () => {
    let nav = document.querySelector('.navbar')
    nav.innerHTML = `
    {%load static%}
    <div class="logo">
            <a href=".html"><img src="{% static 'img/Picture1.png'%}" alt="" class="logo-img"></a>
            <div class="nav-item">
                <div class="search">
                    <input type="text" placeholder="search pet name or food or products" class="search-box">
                    <input type="button" value="search" class="search-btn">
                </div>
            
                <a class="a">
                <img src="img/user.png" id="user-img" alt="">
                <div class="login-logout-pop hide">
                    <p class="account-info">Log in as, name</p>
                    <button type="logout" class="btn" id="user-btn">Log out</button>
                </div>
                </a>

                <!--
                <div class="login-logout-pop hide">
                    <p class="account-info">Log in to place order</p>
                    <button type="login" class="btn" id="user-btn">Log in</button>
                </div>
                -->
                

                <a href="card.html" class="a"><img src="img/cart.png" alt=""></a>
            </div>
        </div>
        <ul class="links-container">
            <li class="links-item"><a href="index.html" class="link">Home</a></li>
            <li class="links-item"><a href="product.html" class="link">Dog</a></li>
            <li class="links-item"><a href="product.html" class="link">Cat</a></li>
            <li class="links-item"><a href="add-product.html" class="link">add Product</a></li>
            <li class="links-item"><a href="seller.html" class="link">Seller</a></li>
        </ul>
    `
}
const createFoot = () => {
    let nav = document.querySelector('.foot')
    nav.innerHTML = `
    <div class="footer-content">
            <img src="img/Picture1.png" alt="" class="foot-logo">
            <div class="footer-ul-category">
                <ul class="category">
                    <li class="category-title">Cat</li>
                    <li><a href="#" class="footerlink">Cats</a></li>
                    <li><a href="#" class="footerlink">Food</a></li>
                    <li><a href="#" class="footerlink">Cages</a></li>
                    <li><a href="#" class="footerlink">vitmens</a></li>
                    <li><a href="#" class="footerlink">clothes</a></li>
                    <li><a href="#" class="footerlink">accessories</a></li>
                </ul>
                <ul class="category">
                    <li class="category-title">Dog</li>
                    <li><a href="#" class="footerlink">Dogs</a></li>
                    <li><a href="#" class="footerlink">Food</a></li>
                    <li><a href="#" class="footerlink">Cages</a></li>
                    <li><a href="#" class="footerlink">vitmens</a></li>
                    <li><a href="#" class="footerlink">clothes</a></li>
                    <li><a href="#" class="footerlink">accessories</a></li>
                </ul>
            </div>
        </div>
        <p class="footer-title">about our team</p>
        <p class="info">Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorem quibusdam o
            fficia neque aliquid laudantium voluptate dolores, nostrum commodi soluta quae minima 
            itaque inventore fuga, impedit incidunt, quis eum nihil enim.</p>
        <p class="info">support Email:hazem12@gmail.com</p>
        <p class="info">tel :12589545521</p>
        <div class="footer-social-conatiner">
			<div>
				<a href="#" class="social-link">term & services</a>
				<a href="#" class="social-link">privacy page</a>
			</div>
			<div>
				<a href="#" class="social-link">facebook</a>
				<a href="#" class="social-link">Twitter</a>
				<a href="#" class="social-link">instgram</a>
			</div>
		</div>
        <p class="footer-credit">best online pet shop in egypt </p>
    `
}

// createnav()
// createFoot()

//create popup
const usrimgbtn = document.querySelector('#user-img')
const usrpop = document.querySelector('.login-logout-pop')
const poptxt = document.querySelector('.account-info')
const actionbtn = document.querySelector('#user-btn')

usrimgbtn.addEventListener('click', () => {
    usrpop.classList.toggle('hide')
})

search_box = document.getElementsByName('product_name')
search_box[0].classList.add('search-box')

span_menu = document.querySelector('#menu-span')
menu = document.querySelector('.side-container');
customMenu = document.querySelector('.menu-custom')
all_heddin = document.querySelector('.all-heddin')
// console.log(menu)

function disPlay(){
    if(counter %2 == 0 ){
        customMenu.style.display = 'flex'
        span_menu.innerHTML = 'close'
        all_heddin.style.display = 'block'
    }else{
        customMenu.style.display = 'none'
        span_menu.innerHTML = 'menu'
        all_heddin.style.display = 'none'
    }
    counter++;
}

counter = 0;
menu.addEventListener('click' , () => {
    disPlay()
})
all_heddin.addEventListener('click', () =>{
    disPlay()
})

function getCookie(name) {
    // Split cookie string and get all individual name=value pairs in an array
    var cookieArr = document.cookie.split(";");

    // Loop through the array elements
    for(var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");

        /* Removing whitespace at the beginning of the cookie name
        and compare it with the given string */
        if(name == cookiePair[0].trim()) {
            // Decode the cookie value and return
            return decodeURIComponent(cookiePair[1]);
        }
    }

    // Return null if not found
    return null;
}


function uuidv4(){
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,function(c){
        var r = Math.random()*16 |0 , v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16)
    })
}

let device = getCookie('device')
if (device == null || device == undefined){
    device = uuidv4()
}
document.cookie = 'device=' + device + ";domine=;path=/"
// console.log('device:' , device)
