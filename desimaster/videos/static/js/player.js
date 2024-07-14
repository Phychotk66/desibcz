const videoPlayer = document.getElementById('video-player');
        const resolutionSelect = document.getElementById('resolution-select');
    
        const player = dashjs.MediaPlayer().create();
        player.initialize(videoPlayer, null, true);
    
        resolutionSelect.addEventListener('change', () => {
            const selectedOption = resolutionSelect.options[resolutionSelect.selectedIndex];
            const manifestUrl = selectedOption.value;
            const width = selectedOption.dataset.width;
            const height = selectedOption.dataset.height;
    
            player.attachSource(manifestUrl);
            videoPlayer.width = width;
            videoPlayer.height = height;
        });
    
        // Set the initial resolution
        const initialOption = resolutionSelect.options[0];
        const initialManifestUrl = initialOption.value;
        const initialWidth = initialOption.dataset.width;
        const initialHeight = initialOption.dataset.height;
    
        player.attachSource(initialManifestUrl);
        videoPlayer.width = initialWidth;
        videoPlayer.height = initialHeight;