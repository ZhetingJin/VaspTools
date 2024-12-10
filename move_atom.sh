#!/bin/bash

# Input file
input_file="POSCAR"
output_file="POSCAR_REV"

# Process the file
awk '
    BEGIN { processing = 0; }
    /Cartesian/ { processing = 1; print; next; }
    processing && NF >= 3 {
        # Update the third column with precise formatting
        $3 = sprintf("%.16f", $3 + 10);
        print $1, $2, $3, (NF > 3 ? $4 : "");
        next;
    }
    { print; }
' "$input_file" > "$output_file"

echo "Processing complete. Modified data is saved in $output_file."
