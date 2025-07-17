document.querySelectorAll('.toggle-block .toggle-header').forEach(header => {
            header.addEventListener('click', function() {
                const block = this.closest('.toggle-block');
                block.classList.toggle('collapsed');
            });
        });