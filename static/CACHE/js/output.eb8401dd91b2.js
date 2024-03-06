fetch('/api-v1/home-banners/').then(response=>response.json()).then(data=>{const productSlider=document.getElementById('product-slider');if(data.length>0&&data[0].product.length>0){const banner=data[0];const products=banner.product;products.forEach(product=>{const slide=document.createElement('div');slide.classList.add('row','single-slide','align-items-center','d-flex');const contentCol=document.createElement('div');contentCol.classList.add('col-lg-5','col-md-6');const bannerContent=document.createElement('div');bannerContent.classList.add('banner-content');const title=document.createElement('h1');title.textContent=product.title;const description=document.createElement('p');description.textContent=product.description;const addButton=document.createElement('a');addButton.classList.add('add-btn');addButton.href="/products/";addButton.innerHTML='<span class="lnr lnr-cross"></span>';const addText=document.createElement('span');addText.classList.add('add-text','text-uppercase');addText.textContent='Shop Now';const imgCol=document.createElement('div');imgCol.classList.add('col-lg-7');const bannerImg=document.createElement('div');bannerImg.classList.add('banner-img');const productImage=document.createElement('img');productImage.classList.add('img-fluid');productImage.src=product.images.length>0?product.images[0].image:'/static/img/banner/banner-img.png';productImage.alt=product.title;addButton.appendChild(addText);bannerContent.appendChild(title);bannerContent.appendChild(description);bannerContent.appendChild(addButton);contentCol.appendChild(bannerContent);bannerImg.appendChild(productImage);imgCol.appendChild(bannerImg);slide.appendChild(contentCol);slide.appendChild(imgCol);productSlider.appendChild(slide);});}}).catch(error=>console.error('Error fetching data:',error));;