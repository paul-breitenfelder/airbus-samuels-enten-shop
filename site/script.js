const productList = document.getElementById('productList');

function formatPrice(price) {
    return new Intl.NumberFormat('de-DE', {
        style: 'currency',
        currency: 'EUR'
    }).format(price);
}

function fetchProducts() {
    if (!productList) {
        return;
    }

    productList.textContent = 'Produkte werden geladen …';

    fetch('/api/products')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(products => {
            productList.replaceChildren(...products.map(product => {
                const productCard = document.createElement('article');
                productCard.className = 'product-card';

                const image = document.createElement('img');
                image.src = product.image;
                image.alt = product.name;

                const title = document.createElement('h3');
                title.textContent = product.name;

                const description = document.createElement('p');
                description.textContent = product.description;

                const price = document.createElement('strong');
                price.textContent = formatPrice(product.price);

                productCard.append(image, title, description, price);

                if (product.sourceUrl && product.imageCredit) {
                    const credit = document.createElement('a');
                    credit.className = 'image-credit';
                    credit.href = product.sourceUrl;
                    credit.target = '_blank';
                    credit.rel = 'noreferrer';
                    credit.textContent = product.imageCredit;
                    productCard.append(credit);
                }

                return productCard;
            }));
        })
        .catch(error => {
            productList.textContent = 'Produkte konnten nicht geladen werden. Versuch es später noch einmal.';
            console.error('Error fetching products:', error);
        });
}

document.addEventListener('DOMContentLoaded', fetchProducts);
