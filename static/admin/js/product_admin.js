(function($) {
    $(document).ready(function() {
        // Function to update value_feature options based on the selected main_feature
        function updateValueFeatureOptions() {
            var mainFeatureField = $('#id_collection__main_feature');
            var valueFeatureField = $('#id_value_feature');

            // Fetch the selected main_feature value
            var mainFeatureValue = mainFeatureField.val();

            // Send a request to get the filtered value features
            $.ajax({
                url: '/admin/get_filtered_feature_values/',  // Change the URL based on your project structure
                data: {
                    main_feature: mainFeatureValue
                },
                success: function(data) {
                    // Update the options in the value_feature field
                    valueFeatureField.empty();
                    $.each(data, function(key, value) {
                        valueFeatureField.append('<option value="' + key + '">' + value + '</option>');
                    });
                }
            });
        }

        // Attach the update function to the change event of main_feature field
        $('#id_collection__main_feature').change(updateValueFeatureOptions);

        // Trigger the change event on page load to initialize the options
        updateValueFeatureOptions();
    });
})(django.jQuery);