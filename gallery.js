const galleries = {
    lic: [
        'gallery/LIC/IMG_20220126_121915.jpg',
        'gallery/LIC/IMG_20220126_121917.jpg',
        'gallery/LIC/IMG_20220126_121922.jpg'
    ],
    massoorie: [
        'gallery/Massoorie/WhatsApp%20Image%202025-07-21%20at%2021.25.23_62140579.jpg',
        'gallery/Massoorie/WhatsApp%20Image%202025-07-21%20at%2022.00.22_5311686d.jpg',
        'gallery/Massoorie/WhatsApp%20Image%202025-07-21%20at%2021.25.20_97fadc99.jpg',
        'gallery/Massoorie/WhatsApp%20Image%202025-07-21%20at%2022.00.23_178661fb.jpg',
        'gallery/Massoorie/WhatsApp%20Image%202025-07-21%20at%2021.25.20_96091b58.jpg',
        'gallery/Massoorie/scenes/WhatsApp%20Image%202025-07-21%20at%2022.00.46_2e5919b1.jpg',
        'gallery/Massoorie/scenes/WhatsApp%20Image%202025-07-21%20at%2022.00.43_93ed5175.jpg',
        'gallery/Massoorie/scenes/WhatsApp%20Image%202025-07-21%20at%2022.00.50_894cba54.jpg',
        'gallery/Massoorie/scenes/WhatsApp%20Image%202025-07-21%20at%2022.00.26_36f132a5.jpg',
        'gallery/Massoorie/scenes/WhatsApp%20Image%202025-07-21%20at%2022.00.37_adb789be.jpg',
        'gallery/Massoorie/scenes/WhatsApp%20Image%202025-07-21%20at%2022.00.52_51e9d8c3.jpg'
    ],
    tirupati: [
        'gallery/Tirupati/IMG_20241231_093309.jpg',
        'gallery/Tirupati/IMG20241231082559.jpg',
        'gallery/Tirupati/IMG_20241231_093632.jpg'
    ],
    cherished: [
        'gallery/cherished%20Moments/IMG_20240218_190811.jpg',
        'gallery/cherished%20Moments/IMG20220717165955.jpg',
        'gallery/cherished%20Moments/IMG20220522064025.jpg',
        'gallery/cherished%20Moments/Snapchat-1972355449.jpg',
        'gallery/cherished%20Moments/IMG_20240218_203104.jpg',
        'gallery/cherished%20Moments/IMG20220702162345.jpg',
        'gallery/cherished%20Moments/IMG_20240101_145355.jpg',
        'gallery/cherished%20Moments/IMG_20240218_183846.jpg',
        'gallery/cherished%20Moments/IMG_20240412_011500.jpg',
        'gallery/cherished%20Moments/IMG20240218142458.jpg',
        'gallery/cherished%20Moments/IMG20240218144341_01.jpg',
        'gallery/cherished%20Moments/IMG20220522063600.jpg'
    ]
};

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.slider').forEach(slider => {
        const galleryName = slider.getAttribute('data-gallery');
        const images = galleries[galleryName];
        let index = 0;
        const img = slider.querySelector('img');

        slider.querySelector('.prev').addEventListener('click', () => {
            index = (index - 1 + images.length) % images.length;
            img.src = images[index];
        });

        slider.querySelector('.next').addEventListener('click', () => {
            index = (index + 1) % images.length;
            img.src = images[index];
        });
    });
});
