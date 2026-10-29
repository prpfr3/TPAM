// Initialize TinyMCE for all textareas with tinymce-editor class
(function () {
  function initTinyMCE() {
    var editors = document.querySelectorAll('textarea.tinymce-editor');
    editors.forEach(function (textarea) {
      // Skip if already initialized
      if (tinymce.get(textarea.id)) {
        return;
      }

      tinymce.init({
        target: textarea,
        plugins: [
          'advlist',
          'autolink',
          'lists',
          'link',
          'image',
          'charmap',
          'preview',
          'anchor',
          'searchreplace',
          'visualblocks',
          'code',
          'fullscreen',
          'insertdatetime',
          'media',
          'table',
          'help',
          'wordcount',
        ],
        toolbar:
          'undo redo | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | code fullscreen | help',
        height: 300,
        menubar: true,
      });
    });
  }

  // Initialize on document ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      // Wait for tinymce to be loaded
      if (typeof tinymce !== 'undefined') {
        initTinyMCE();
      } else {
        setTimeout(initTinyMCE, 100);
      }
    });
  } else {
    // DOM is already loaded
    if (typeof tinymce !== 'undefined') {
      initTinyMCE();
    } else {
      setTimeout(initTinyMCE, 100);
    }
  }

  // Re-initialize when Django adds new inline forms
  if (typeof django !== 'undefined' && typeof django.jQuery !== 'undefined') {
    django
      .jQuery(document)
      .on('formset:added', function (e, $row, formsetName) {
        var newTextareas = $row.find('textarea.tinymce-editor');
        newTextareas.each(function () {
          // Remove the id to force TinyMCE to generate a new one
          this.id = '';
          tinymce.init({
            target: this,
            plugins: [
              'advlist',
              'autolink',
              'lists',
              'link',
              'image',
              'charmap',
              'preview',
              'anchor',
              'searchreplace',
              'visualblocks',
              'code',
              'fullscreen',
              'insertdatetime',
              'media',
              'table',
              'help',
              'wordcount',
            ],
            toolbar:
              'undo redo | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | code fullscreen | help',
            height: 300,
            menubar: true,
          });
        });
      });
  }
})();
