function toggleDetails(section) {
    // Hide both details sections first
    document.getElementById('submitted').style.display = 'none';
    document.getElementById('not-submitted').style.display = 'none';

    // Show the clicked section
    document.getElementById(section).style.display = 'block';
}

