document.addEventListener('DOMContentLoaded', function () {

    const addButton = document.getElementById('add-social-link');

    const totalForms = document.getElementById(
        'id_social_links-TOTAL_FORMS'
    );

    const formsContainer = document.getElementById('social-links');

    const emptyForm = document.getElementById('empty-form').innerHTML;

    addButton.addEventListener('click', function () {

        const formCount = parseInt(totalForms.value);

        const newFormHtml = emptyForm.replace(
            /__prefix__/g,
            formCount
        );

        formsContainer.insertAdjacentHTML(
            'beforeend',
            newFormHtml
        );

        totalForms.value = formCount + 1;
    });

});
