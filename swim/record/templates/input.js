<script>
  $(function() {
    $('form').on('click', '#one_more', function() {

      var m_10 = $('.m_10:eq(-1) option:selected').val();
      var m_1 = $('.m_1:eq(-1) option:selected').val();
      var s_10 = $('.s_10:eq(-1) option:selected').val();
      var s_1 = $('.s_1:eq(-1) option:selected').val();
      var ms_10 = $('.ms_10:eq(-1) option:selected').val();
      var ms_1 = $('.ms_1:eq(-1) option:selected').val();

      var lastform = $('#result > li:eq(-1)').clone();
      lastform.find('.m_10').val(m_10);
      lastform.find('.m_1').val(m_1);
      lastform.find('.s_10').val(s_10);
      lastform.find('.s_1').val(s_1);
      lastform.find('.ms_10').val(ms_10);
      lastform.find('.ms_1').val(ms_1);

      $('#result').append(lastform);
    });
  });
</script>
