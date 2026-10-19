const platform = navigator.userAgentData?.platform || navigator.platform || '';
const key = /Android/i.test(navigator.userAgent) ? 'android' : /Win/i.test(platform) ? 'windows' : /Mac/i.test(platform) ? 'macos' : /Linux/i.test(platform) ? 'linux' : null;
const card = key && document.querySelector(`[data-platform="${key}"]`);
if (card) { card.classList.add('preferred'); card.querySelector('.recommendation').hidden = false; }
function showInstallation() {
  const id = location.hash.slice(1);
  if (!id.startsWith('install-')) return;
  const details = document.getElementById(id);
  if (details?.tagName === 'DETAILS') details.open = true;
}
window.addEventListener('hashchange', showInstallation);
showInstallation();
