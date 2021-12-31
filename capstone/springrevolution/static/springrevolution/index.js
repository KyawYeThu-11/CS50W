document.addEventListener('DOMContentLoaded', function(){
    
    // For nav_tab to work
    document.querySelectorAll('.tabs').forEach(tab =>{
        tab.onclick = function(){
            show_page(this.dataset.page);
        }
    })

    // for tooltips & toasts to work
    $("body").tooltip({ selector: '[data-toggle=tooltip]' }); // note that the attribute is 'data-toggle', NOT 'data-bs-toggle'
    $('.toast').toast('show');
})

function show_page(page){
    
    const home_page = document.querySelector('.home-page').style;
    const other_page = document.querySelector('.other-pages').style;

    // make active tab distinct
    document.querySelectorAll('.tabs').forEach(tab => {
        tab.setAttribute('data-active', 'False');
        if (tab.dataset.page === page){
            tab.setAttribute('data-active', 'True');
        }
    })

    if(page === 'home'){
        home_page.display = 'block';
        other_page.display = 'none';
    }
    else{
        fetch(`/pages/${page}`)
        .then(response => response.text())
        .then(text => {
            home_page.display = 'none';
            other_page.display = 'block';
            document.querySelector('.other-pages').innerHTML = text;
            
            // which sub-tab will be shown as a default
            if(page === "donations"){
                show_content('categories_content')  
            }

            // for mini-tabs to work
            document.querySelectorAll('.mini_tabs').forEach(tab =>{
                tab.onclick = function(){
                    content = tab.dataset.content;
                    show_content(content);
                }
            })

            // for category cards' hover design
            document.querySelectorAll('.category').forEach(card =>{
                card.onmouseover = function(){
                    change_button(card, "show");
                }
                card.onmouseout = function(){
                    change_button(card, "hide");
                }
            })

            // requesting a list of links after clicking a particular category
            document.querySelectorAll('.support-btn').forEach(button => {
                button.onclick = function(){
                    show_page('links'); // request_links function will not wait this show_page function, containing fetch, to be done 
                    request_links(this.dataset.buttonid);
                }
            })

            // unless login, submit button doesn't work
            document.querySelectorAll('.diabled_button').forEach(button => {
                button.onclick = function(){
                    return false;
                }
            })
            console.log(page);
        })
    }  
}

function show_content(content){
    document.querySelectorAll('.mini_tabs').forEach(tab =>{
        tab.setAttribute('data-active', 'False');
        if (tab.dataset.content === content){
            tab.setAttribute('data-active', 'True');
        }
    })

    document.querySelectorAll('.contents').forEach(content=>{
        content.style.display = "none";
    })
    document.querySelector(`#${content}`).style.display = 'block';
}

function change_button(div, action){
    const id = div.dataset.buttonid;
    const button = document.querySelector(`#${id}`);

    if(action === 'show'){
        div.style.opacity = "0.8";
        button.style.opacity = "1";
        div.style.transition = "opacity 1s";
        button.style.transition = "opacity 1s";
    }else{
        div.style.opacity = "1";
        button.style.opacity = "0.0";
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
  
async function request_links(buttonid) {
    await sleep(1000);
  
    fetch(`/request_links/${buttonid}`)
    .then(request => request.json())
    .then(links => {

        var category = null;
        var count = 1;
        links.forEach(link =>{
            const name = link.name;
            const url = link.url;
            const description = link.description;
            const source = link.source;
            category = category_name(link.category);
            var date = link.date;

            if (date === null){
                date = '';
            }
            
            // Creating an accordion item
            const accordion_item = document.createElement('div');
            accordion_item.className = "accordion-item";
        
            const accordion_header = document.createElement('h2');
            accordion_header.className = "accordion-header";
            accordion_header.setAttribute('id', `heading${count}`);
        
            const button = document.createElement('button');
            button.className = "accordion-button";
            setAttributes(button, {'type':'button', 'data-bs-toggle':'collapse', 'data-bs-target':`#collapse${count}`, 'aria-expanded':'true', 'aria-controls':`collapse${count}`});
            if (source === 'facebook'){
                button.innerHTML = `<div class='col-xl-10 col-9'>${count}. ${name} &nbsp; <span class="badge rounded-pill bg-primary">Facebook</span></div><div class='col-xl-1 col-2'>${date}</div>`;
            }else if(source === 'twitter'){
                button.innerHTML = `<div class='col-xl-10 col-9'>${count}. ${name} &nbsp; <span class="badge rounded-pill bg-info">Twitter</span></div><div class='col-xl-1 col-2'>${date}</div>`;
            }else if(source === 'instagram'){
                button.innerHTML = `<div class='col-xl-10 col-9'>${count}. ${name} &nbsp; <span class="badge rounded-pill bg-warning">Instagram</span></div><div class='col-xl-1 col-2'>${date}</div>`;           
            }else{
                button.innerHTML = `<div class='col-xl-10 col-9'>${count}. ${name} &nbsp; <span class="badge rounded-pill bg-success">Website</span></div><div class='col-xl-1 col-2'>${date}</div>`;               
            }
            
            const accordion_text = document.createElement('div');
            accordion_text.className = 'accordion-collapse collapse';
            setAttributes(accordion_text, {'id':`collapse${count}`, 'aria-labelledby':`heading${count}`, 'data-bs-parent':'#accordionExample'})
            
            const accordion_body = document.createElement('div');
            accordion_body.className = 'accordion-body';
            if (description === ''){
                accordion_body.innerHTML = 
                `Description - N/A <br><br>
                <a href="${url}" type="button" class="btn btn-success btn-sm btn-visit" data-toggle="tooltip" data-bs-placement="right" title="${url}">Visit</a>
                `;
            }else{
                accordion_body.innerHTML = 
                `<strong>Description</strong><br> ${description}<br><br>
                <a href="${url}" type="button" class="btn btn-success btn-sm btn-visit" data-toggle="tooltip" data-bs-placement="right" title="${url}">Visit</a>
                `;                
            }
                    
            accordion_header.appendChild(button);
            accordion_text.appendChild(accordion_body);
        
            accordion_item.appendChild(accordion_header);
            accordion_item.appendChild(accordion_text);
            
            document.querySelector('.links_accordion').append(accordion_item);
            count++;            
        })
        document.querySelector('.category-name').innerHTML = `Category: ${category}`;
    })
}

function setAttributes(el, attrs) {
    for(var key in attrs) {
      el.setAttribute(key, attrs[key]);
    }
}

function category_name(category){
    if (category === 'CDM'){
        return 'Civil Disobedience Movement'
    }else if (category === 'Refugees'){
        return 'Ethnic Minorities & Refugees'
    }else if (category === 'Revolutionaries'){
        return 'Revolution Victims & Heroes'
    }else{
        return category
    }
}