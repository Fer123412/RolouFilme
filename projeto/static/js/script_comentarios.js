document.querySelectorAll(".btn_responder").forEach((btn) => {
  btn.addEventListener("click", () => {
    const form = document.getElementById(btn.dataset.alvo);
    form.hidden = !form.hidden;
    if (!form.hidden) form.querySelector("textarea").focus();
  });
});
