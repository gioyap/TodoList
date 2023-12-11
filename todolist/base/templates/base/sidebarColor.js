    // Load the saved color or use a default color
    const savedColor = localStorage.getItem('headerBarColor');
    const sidebar = document.getElementById('sidebar');
    sidebar.style.backgroundColor = savedColor || '#12b8ce';

    function toggleColorOptions() {
        const colorOptions = document.getElementById('colorOptions');
        colorOptions.style.display = colorOptions.style.display === 'none' ? 'block' : 'none';
    }

    function changeHeaderColor(color) {
        sidebar.style.backgroundColor = color;
        localStorage.setItem('headerBarColor', color);
        // Optionally, hide the color options after a color is selected
        document.getElementById('colorOptions').style.display = 'none';
    }
    function toggleSidebar() {
            const sidebar = document.querySelector('.sidebar');
            sidebar.classList.toggle('show');
        }
    function toggleDropdown(dropdownId) {
        var dropdown = document.getElementById(dropdownId + 'Dropdown');
        dropdown.style.display = (dropdown.style.display === 'block') ? 'none' : 'block';
    } 