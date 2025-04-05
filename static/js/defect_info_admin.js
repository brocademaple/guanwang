document.addEventListener('DOMContentLoaded', function () {
  const soilTypeSelect = document.getElementById('id_soil_type');
  const wetLoessLevelSelect = document.getElementById('id_wet_loess_level');
  const expansiveSoilLevelSelect = document.getElementById('id_expansive_soil_level');
  const siltTypeSelect = document.getElementById('id_silt_type');

  function hideAllSelects() {
      wetLoessLevelSelect.style.display = 'none';
      expansiveSoilLevelSelect.style.display = 'none';
      siltTypeSelect.style.display = 'none';
  }

  function updateSelectVisibility() {
      const soilType = soilTypeSelect.value;
      hideAllSelects();
      switch (soilType) {
          case '湿陷性黄土':
              wetLoessLevelSelect.style.display = 'block';
              break;
          case '膨胀土':
              expansiveSoilLevelSelect.style.display = 'block';
              break;
          case '淤泥类土':
              siltTypeSelect.style.display = 'block';
              break;
          default:
              break;
      }
  }

  soilTypeSelect.addEventListener('change', updateSelectVisibility);
  updateSelectVisibility();
});