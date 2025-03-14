<?php
/**
 * Plugin Name: My Photo Importer
 * Description: A WP-CLI command to import WooCommerce products with ACF fields from a CSV.
 * Version: 1.0
 * Author: Your Name
 */

if (defined('WP_CLI') && WP_CLI) {
    WP_CLI::add_command('myplugin import-photo-products', function() {
        $file = 'D:\OneDrive\Documents\Bluebell Railway\Archive Maps and Plans Database\BRMPhotos.csv';
        
        if (!file_exists($file)) {
            WP_CLI::error("File not found: $file");
        }

        // Open the file with UTF-8 encoding and handle BOM
        $csv_content = file_get_contents($file);
        // Remove BOM if it exists
        if (substr($csv_content, 0, 3) === "\xef\xbb\xbf") {
            $csv_content = substr($csv_content, 3);
        }
        
        // Convert the content back to an array
        $csv = array_map('str_getcsv', explode("\n", $csv_content));
        $headers = array_shift($csv);

        $created = 0;
        $skipped = 0;

        WP_CLI::line("CSV headers: " . implode(', ', $headers)); // Debugging headers

        foreach ($csv as $row) {
            // Debugging the row contents
            WP_CLI::line("Processing row: " . implode(', ', $row));

            $data = array_combine($headers, $row);
            $reference_number = trim($data['Reference Number']); // Trim any unwanted spaces or BOM

            // Debugging the reference number
            WP_CLI::line("Reference Number: '$reference_number'");

            // Skip if Reference Number is empty
            if (empty($reference_number)) {
                WP_CLI::warning("Skipping product due to missing Reference Number.");
                $skipped++;
                continue;
            }

            // Check if product already exists
            $existing_product = wc_get_product_id_by_sku($reference_number);
            if ($existing_product) {
                WP_CLI::warning("Product with Reference Number '{$reference_number}' already exists (ID: $existing_product), skipping.");
                $skipped++;
                continue;
            }

            // Create the WooCommerce product
            $product = new WC_Product_Simple();
            $product->set_name($data['Class'] . ' at ' . $data['Location']);
            $product->set_description("Class: {$data['Class']} | Location: {$data['Location']} | Train Working: {$data['Train Working']}");
            $product->set_regular_price('2.50');
            $product->set_sku($reference_number);
            $product_id = $product->save();

            if (!$product_id) {
                WP_CLI::error("Failed to create product for Reference Number: {$reference_number}");
            }

            // Calculate URL and store it in the ACF field
            $first_three = substr($reference_number, 0, 3);
            $last_three = substr($reference_number, -3);
            $photo_url = "https://www.bluebell-railway-museum.co.uk/archive/photos2/{$first_three}/{$last_three}.jpg";
            
            // Update ACF fields
            update_field('reference_number', $reference_number, $product_id);
            update_field('key', $data['Key'], $product_id);
            update_field('company', $data['Company'], $product_id);
            update_field('class', $data['Class'], $product_id);
            update_field('date', $data['Date'], $product_id);
            update_field('number', $data['Number'], $product_id);
            update_field('name', $data['Name'], $product_id);
            update_field('location', $data['Location'], $product_id);
            update_field('train_working', $data['Train Working'], $product_id);
            update_field('other_information', $data['Other information'], $product_id);
            update_field('photographer', $data['Photographer'], $product_id);
            update_field('photographers_ref', isset($data["Photographer's Ref"]) ? $data["Photographer's Ref"] : '', $product_id);
            update_field('sort_date', $data['Sort Date'], $product_id);
            update_field('day_of_week', $data['Day of Week'], $product_id);
            update_field('holiday', $data['Holiday'], $product_id);
            update_field('image_url', $photo_url, $product_id);

            WP_CLI::success("Created new product with Reference Number: {$reference_number} (ID: $product_id)");
            $created++;
        }

        WP_CLI::success("Import completed. Created: $created, Skipped: $skipped.");
    });
}
