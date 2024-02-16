let currentCollectionsId=null;let currentUnitPriceGt=null;let currentUnitPriceLt=null;let currentSearch=null;let currentOrdering=null;let currentFeatureKey=null;let currentFeatureValue=null;let currentSecondHand=null;let selectedProducts=[];console.log(selectedProducts)
const compareButtonClicked=(productId)=>{const index=selectedProducts.indexOf(productId);if(index===-1){selectedProducts.push(productId);}else{selectedProducts.splice(index,1);}
console.log('Selected products:',selectedProducts);}
function createSocialInfo(iconClass,text,moreClass=null){const socialInfo=document.createElement('button');socialInfo.classList.add('social-info');const iconSpan=document.createElement('span');iconSpan.classList.add(iconClass);iconSpan.classList.add(moreClass);const hoverText=document.createElement('p');hoverText.classList.add('hover-text');hoverText.textContent=text;socialInfo.appendChild(iconSpan);socialInfo.appendChild(hoverText);return socialInfo;}
const productsPerPage=1;let currentPage=1;function fetchProducts(page=1,selectedOption='updated_at',collectionsId=null,unit_price__gt=null,unit_price__lt=null,search=null,feature_key=null,feature_value=null,secondhand=null){let apiUrl=null
apiUrl=`/shop/products/?page=${page}&ordering=${getSortingOrdering(selectedOption)}`;if(collectionsId!=null){apiUrl+=`&collection_id=${collectionsId}`;addFilterToCurrentFilters('مجموعه',collectionsId);}
if(selectedOption!=null){apiUrl+=`&ordering=${getSortingOrdering(selectedOption)}`;addFilterToCurrentFilters('ترتیب',selectedOption);}
if(unit_price__gt!=null){apiUrl+=`&unit_price__gt=${unit_price__gt}`;addFilterToCurrentFilters('قیمت بیشتر از ',unit_price__gt);}
if(unit_price__lt!=null){apiUrl+=`&unit_price__lt=${unit_price__lt}`;addFilterToCurrentFilters('قیمت کمتر از ',unit_price__lt);}
if(search!=null){apiUrl+=`&search=${search}`;addFilterToCurrentFilters('جستجو',search);}
if(feature_key!=null){apiUrl+=`&feature_key=${feature_key}`;addFilterToCurrentFilters('کلید ویژگی',feature_key);}
if(feature_value!=null){apiUrl+=`&feature_value=${feature_value}`;addFilterToCurrentFilters('مقدار ویژگی',feature_value);}
if(secondhand!=null){apiUrl+=`&secondhand=${secondhand}`;addFilterToCurrentFilters('SecondHand',secondhand);}
console.log(apiUrl)
fetch(apiUrl).then(response=>response.json()).then(products=>{const productContainer=document.getElementById('productContainer');productContainer.innerHTML='';products.results.forEach(product=>{{const currentLanguage='fa';const productBlock=document.createElement('div');productBlock.classList.add('col-lg-4','col-md-6','single-product');const productImage=document.createElement('img');productImage.classList.add('img-fluid');productImage.src=product.images.length>0?product.images[0].image:'/static/img/default-product.jpg';productImage.alt=product.title;const productDetails=document.createElement('div');productDetails.classList.add('product-details');const productName=document.createElement('h6');productName.textContent=product.title;const productPrice=document.createElement('div');productPrice.classList.add('price');const originalPrice=document.createElement('h6');originalPrice.textContent=`$${product.price.toFixed(2)}`;const discountedPrice=document.createElement('h6');if(product.org_price!==product.price){discountedPrice.classList.add('l-through');discountedPrice.textContent=`$${product.org_price.toFixed(2)}`;}
const productActions=document.createElement('div');productActions.classList.add('prd-bottom');const addToBag=createSocialInfo('ti-bag','اضافه کردن به سبد ','ti-bag');addToBag.addEventListener('click',()=>{const cartId=localStorage.getItem('cartId');const productId=product.id;const quantity=1;if(!cartId||cartId==undefined){createCartAndAddToBag(productId);}else{addToCart(cartId,productId,quantity);}});const viewMore=createSocialInfo('lnr','توضیحات','lnr-move');viewMore.addEventListener('click',()=>{const productId=product.id;window.location.href=`/products/${productId}/`;});const compare=createSocialInfo('lnr','مقایسه','lnr-sync');compare.addEventListener('click',()=>{compareButtonClicked(product.id);});productDetails.appendChild(productName);productPrice.appendChild(originalPrice);if(discountedPrice.textContent.trim()!==''){productPrice.appendChild(discountedPrice);}
productDetails.appendChild(productPrice);productActions.appendChild(addToBag);productActions.appendChild(viewMore);productActions.appendChild(compare);productBlock.appendChild(productImage);productBlock.appendChild(productDetails);productBlock.appendChild(productActions);productContainer.appendChild(productBlock);productContainer.appendChild(productBlock);}});updatePagination(products.count,productsPerPage);}).catch(error=>{console.error('Error fetching products:',error);});function addFilterToCurrentFilters(filterName,filterValue){const existingButton=Array.from(document.querySelectorAll('#Filters button')).find(button=>{return button.textContent.startsWith(`${filterName}:`);});if(existingButton){existingButton.textContent=`${filterName}: ${filterValue}`;if(filterName=='کلید ویژگی'){const elements=document.querySelectorAll('.btn.btn-sm.btn-primary.mr-2')
console.log(elements)
for(let i=0;i<elements.length;i++){console.log(elements[i])
if(elements[i].textContent.includes('مقدار ویژگی')){console.log('findddddd2')
elements[i].remove();}}}}else{switch(filterName){case'مجموعه':currentCollectionsId=filterValue;break;case'ترتیب':currentOrdering=filterValue;break;case'قیمت بیشتر از ':currentUnitPriceGt=filterValue;break;case'قیمت کمتر از ':currentUnitPriceLt=filterValue;break;case'جستجو':currentSearch=filterValue;break;case'کلید ویژگی':currentFeatureKey=filterValue;currentFeatureValue=null;break;case'مقدار ویژگی':currentFeatureValue=filterValue;break;case'SecondHand':currentSecondHand=filterValue;break;default:break;}
const filtersContainer=document.getElementById('Filters');const filterButton=document.createElement('button');filterButton.textContent=`${filterName}: ${filterValue}`;filterButton.classList.add('btn','btn-sm','btn-primary','mr-2');filterButton.addEventListener('click',()=>{removeFilterFromApiUrl(filterName,filterValue);if(filterName=='کلید ویژگی'){const elements=document.querySelectorAll('.btn.btn-sm.btn-primary.mr-2')
console.log(elements)
for(let i=0;i<elements.length;i++){console.log(elements[i])
if(elements[i].textContent.includes('مقدار ویژگی')){console.log('findddddd')
filtersContainer.removeChild(elements[i]);}}}
filtersContainer.removeChild(filterButton);currentPage=1;fetchProducts(currentPage,currentOrdering,currentCollectionsId,currentUnitPriceGt,currentUnitPriceLt,currentSearch,currentFeatureKey,currentFeatureValue,currentSecondHand);});filtersContainer.appendChild(filterButton);}}
function removeFilterFromApiUrl(filterName,filterValue){switch(filterName){case'مجموعه':currentCollectionsId=null;break;case'ترتیب':currentOrdering=null;break;case'قیمت بیشتر از ':currentUnitPriceGt=null;break;case'قیمت کمتر از ':currentUnitPriceLt=null;break;case'جستجو':currentSearch=null;break;case'کلید ویژگی':currentFeatureKey=null;currentFeatureValue=null;break;case'مقدار ویژگی':currentFeatureValue=null;break;case'SecondHand':currentSecondHand=null;break;default:break;}}}
function getToken(){return localStorage.getItem('JWT');}
function createCartAndAddToBag(productId){const token=getToken();let headers={'Content-Type':'application/json',};if(token){headers['Authorization']=`JWT ${token}`;}
const options={method:'POST',headers:headers,};console.log('headers',headers)
fetch('/shop/cart/',options).then(response=>response.json()).then(data=>{const cartId=data.id;localStorage.setItem('cartId',cartId);addToCart(cartId,productId,1);}).catch(error=>console.error('Error creating cart:',error));}
function addToCart(cartId,productId,quantity){const token=getToken();let headers={'Content-Type':'application/json',};if(token){headers['Authorization']=`JWT ${token}`;}
fetch(`/shop/cart/${cartId}/items/`,{method:'POST',headers:headers,body:JSON.stringify({product_id:productId,quantity:quantity})}).then(response=>{if(response.ok){console.log('Item added to cart successfully');}else{if(response.status===401){console.error('Unauthorized: Token may be expired or invalid');localStorage.removeItem('JWT');}
console.error('Failed to add item to cart:',response.statusText);createCartAndAddToBag(productId);}}).catch(error=>console.error('Error adding item to cart:',error));}
function updatePagination(totalProducts,productsPerPage){const totalPages=Math.ceil(totalProducts/productsPerPage);const paginationContainer=document.getElementById('paginationContainer');paginationContainer.innerHTML='';for(let i=1;i<=totalPages;i++){const pageLink=document.createElement('button');pageLink.textContent=i;pageLink.addEventListener('click',()=>{currentPage=i;fetchProducts(currentPage,currentOrdering,currentCollectionsId,currentUnitPriceGt,currentUnitPriceLt,currentSearch,currentFeatureKey,currentFeatureValue,currentSecondHand);});if(i===currentPage){pageLink.classList.add('active');}
paginationContainer.appendChild(pageLink);}
if(currentPage>1){const prevLink=createPaginationLink('prev-arrow','fa-long-arrow-left',currentPage-1);paginationContainer.insertBefore(prevLink,paginationContainer.firstChild);}
if(currentPage<totalPages){const nextLink=createPaginationLink('next-arrow','fa-long-arrow-right',currentPage+1);paginationContainer.appendChild(nextLink);}}
function createPaginationLink(className,iconClass,page){const link=document.createElement('button');link.classList.add(className);link.addEventListener('click',()=>{currentPage=page;fetchProducts(currentPage,currentOrdering,currentCollectionsId,currentUnitPriceGt,currentUnitPriceLt,currentSearch,currentFeatureKey,currentFeatureValue,currentSecondHand);});const icon=document.createElement('i');icon.classList.add('fa');icon.classList.add(iconClass);link.appendChild(icon);return link;}
function getSortingOrdering(sortingOption){switch(sortingOption){case'price_asc':return'unit_price';case'price_desc':return'-unit_price';case'best_sales':return'best_sales';default:return'-updated_at';}}
document.addEventListener("DOMContentLoaded",function(){const searchInput=document.getElementById("search_input");searchInput.addEventListener("keypress",function(event){if(event.key==='Enter'){event.preventDefault();const searchQuery=searchInput.value.trim();console.log(searchQuery)
if(searchQuery!==''){currentSearch=searchQuery
currentPage=1
fetchProducts(currentPage,currentOrdering,currentCollectionsId,currentUnitPriceGt,currentUnitPriceLt,currentSearch,currentFeatureKey,currentFeatureValue,currentSecondHand);}}});const lowerValue=document.getElementById('lower-value');const upperValue=document.getElementById('upper-value');let initialLowerValue=lowerValue.textContent;let initialUpperValue=upperValue.textContent;function checkForChanges(){if(lowerValue.textContent!==initialLowerValue){initialLowerValue=lowerValue.textContent;currentUnitPriceGt=parseInt(lowerValue.textContent);console.log('Changed low value:',currentUnitPriceGt);currentPage=1
fetchProducts(currentPage,currentOrdering,currentCollectionsId,currentUnitPriceGt,currentUnitPriceLt,currentSearch,currentFeatureKey,currentFeatureValue,currentSecondHand);}
if(upperValue.textContent!==initialUpperValue){initialUpperValue=upperValue.textContent;currentUnitPriceLt=parseInt(upperValue.textContent);console.log('Changed high value:',currentUnitPriceLt);currentPage=1
fetchProducts(currentPage,currentOrdering,currentCollectionsId,currentUnitPriceGt,currentUnitPriceLt,currentSearch,currentFeatureKey,currentFeatureValue,currentSecondHand);}}
setInterval(checkForChanges,200);});currentPage=1
fetchProducts(currentPage,currentOrdering,currentCollectionsId,currentUnitPriceGt,currentUnitPriceLt,currentSearch,currentFeatureKey,currentFeatureValue,currentSecondHand);const compareButton=document.getElementById('compare-button');compareButton.addEventListener('click',function(){const compareUrl='/compare/?product_ids='+selectedProducts.join('&product_ids=');window.location.href=compareUrl;});const sortingButtonsContainer=document.getElementById("sortingggDropdown");sortingButtonsContainer.addEventListener("click",function(event){if(event.target.tagName==='BUTTON'){const selectedOption=event.target.value;currentOrdering=selectedOption
currentPage=1
fetchProducts(currentPage,currentOrdering,currentCollectionsId,currentUnitPriceGt,currentUnitPriceLt,currentSearch,currentFeatureKey,currentFeatureValue,currentSecondHand);}});fetch('/shop/collections/').then(response=>response.json()).then(data=>{const sidebarCategories=document.querySelector('.sidebar-categories');const div=document.createElement('div');div.classList.add('head');div.textContent='Browse Collecitons'
generateSidebarMenu(data,sidebarCategories);}).catch(error=>console.error('Error fetching data:',error));function generateSidebarMenu(collections,parentElement){const ul=document.createElement('ul');ul.classList.add('main-categories');collections.forEach(collection=>{const li=document.createElement('li');li.classList.add('main-nav-list');const a=document.createElement('a');a.setAttribute('data-toggle','collapse');a.href=`#${collection.title}`;a.setAttribute('aria-expanded','false');a.setAttribute('aria-controls',collection.title);const spanArrow=document.createElement('span');spanArrow.classList.add('lnr','lnr-arrow-right');console.log(collection)
console.log(collection.products_count)
const spanTitle=document.createElement('span');spanTitle.innerHTML=`${collection.title} <span class="number">
                    (${collection.products_count})</span>`;a.appendChild(spanArrow);a.appendChild(spanTitle);a.addEventListener('click',()=>{currentCollectionsId=collection.id
currentPage=1
fetchProducts(currentPage,currentOrdering,currentCollectionsId,currentUnitPriceGt,currentUnitPriceLt,currentSearch,currentFeatureKey,currentFeatureValue,currentSecondHand);});li.appendChild(a);li.appendChild(a);if(collection.children&&collection.children.length>0){generateSidebarMenu(collection.children,li);}
ul.appendChild(li);});parentElement.appendChild(ul);}
fetch('/shop/features/').then(response=>response.json()).then(data=>{const commonFilter=document.querySelector('.common-filter');data.forEach(feature=>{const keyItem=document.createElement('li');keyItem.classList.add('filter-list','text-capitalize','bold');const br=document.createElement('br');const keyHeader=document.createElement('h6');keyHeader.style.cursor='pointer'
keyHeader.textContent=feature.key;const keyProductCount=document.createElement('span');keyProductCount.classList.add('number');keyProductCount.textContent=`(${feature.key_product_count})`;keyHeader.appendChild(keyProductCount);keyItem.appendChild(keyHeader);keyHeader.addEventListener('click',()=>{currentFeatureKey=feature.id;currentFeatureValue=null;currentPage=1
fetchProducts(currentPage,currentOrdering,currentCollectionsId,currentUnitPriceGt,currentUnitPriceLt,currentSearch,currentFeatureKey,currentFeatureValue,currentSecondHand);});const valueList=document.createElement('ul');valueList.classList.add('filter-list','text-capitalize','bold');feature.values.forEach(value=>{const valueItem=document.createElement('li');valueItem.classList.add('filter-list','text-capitalize','bold');const valueHeader=document.createElement('h6');valueHeader.style.cursor='pointer'
valueHeader.textContent=value.value;const valueProductCount=document.createElement('span');valueProductCount.classList.add('number');valueProductCount.textContent=`(${value.product_count})`;valueHeader.appendChild(valueProductCount);valueItem.appendChild(valueHeader);valueItem.addEventListener('click',()=>{currentFeatureKey=feature.id;currentFeatureValue=value.id;currentPage=1
fetchProducts(currentPage,currentOrdering,currentCollectionsId,currentUnitPriceGt,currentUnitPriceLt,currentSearch,currentFeatureKey,currentFeatureValue,currentSecondHand);});valueList.appendChild(valueItem);});keyItem.appendChild(valueList);commonFilter.appendChild(keyItem);keyItem.appendChild(br);});}).catch(error=>console.error('Error fetching features:',error));const secondHandOnlyButton=document.querySelector('#seccondhand button[value="true"]');const newOnlyButton=document.querySelector('#seccondhand button[value="false"]');secondHandOnlyButton.addEventListener('click',function(){currentSecondHand=true;fetchProducts(currentPage,currentOrdering,currentCollectionsId,currentUnitPriceGt,currentUnitPriceLt,currentSearch,currentFeatureKey,currentFeatureValue,currentSecondHand);});newOnlyButton.addEventListener('click',function(){currentSecondHand=false;fetchProducts(currentPage,currentOrdering,currentCollectionsId,currentUnitPriceGt,currentUnitPriceLt,currentSearch,currentFeatureKey,currentFeatureValue,currentSecondHand);});;