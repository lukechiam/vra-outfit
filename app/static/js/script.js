// Load size guide data from JSON file
let sizeOption = null;

async function loadSizeOption() {
  try {
    const response = await fetch('sizeOption.json');
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    sizeOption = await response.json();
    populateSizeOption("longSleeveGreenShirt");
    populateSizeOption("tShirt");
    populateSizeOption("jacket");
    populateSizeOption("rainJacket");
    populateSizeOption("rainPants");
  } catch (error) {
    console.error('Error loading size guide:', error);
    document.getElementById('result').textContent = 'Failed to load size guide data. Please try again.';
  }
}

// Populate clothing type dropdown
function populateSizeOption(clothingType) {
  const clothingTypeSelect = document.getElementById(clothingType);
  // clothingTypeSelect.innerHTML = '<option value="">Select size...</option>';
  if (!sizeOption || !sizeOption["sizes"]) {
    return null;
  }
  sizeOption["sizes"].forEach((item) => {
    const option = document.createElement('option');
    option.value = item;
    option.textContent = item;
    clothingTypeSelect.appendChild(option);
  });
}

// Initialize form on page load
document.addEventListener('DOMContentLoaded', () => {
  loadSizeOption();
});

function toggleImage(x) {
  const image = document.getElementById(x);
  image.style.display = image.style.display === 'none' ? 'block' : 'none';
}
