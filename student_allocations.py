import pandas as pd

# Load CSVs with proper dtypes
students = pd.read_csv('student_details.csv', dtype={'UniqueID': str})
preferences = pd.read_csv('preference_data.csv', dtype={'UniqueID': str, 'CollegeID': str, 'PrefNumber': int})
seats = pd.read_csv('institution_data.csv', dtype={'CollegeID': str})

def seat_column(caste):
    if caste == 'SC':
        return 'SC'
    elif caste == 'ST':
        return 'ST'
    elif caste == 'BC':
        return 'BC'
    elif caste == 'Minority':
        return 'Minority'
    elif caste == 'OC':
        return 'OC'
    elif caste == 'SC-CC':
        return 'SC-CC'
    else:
        return None

output = []

# ✅ Process ALL students (no input, full dataframe)
for idx, srow in students.iterrows():
    uid = str(srow['UniqueID']).strip()
    gender = srow['Gender']
    caste = srow['Caste']
    
    # Get all preferences for this student sorted by PrefNumber
    pset = preferences[preferences['UniqueID'] == uid].sort_values(by='PrefNumber')
    if pset.empty:
        continue
    
    scol = seat_column(caste)
    allocated_college = None
    allocated_pref = None
    
    # Iterate through preferences until seat is found
    for _, pref in pset.iterrows():
        collegeid = str(pref['CollegeID']).strip()
        prefnumber = int(pref['PrefNumber'])
        
        seat_row = seats[seats['CollegeID'] == collegeid]
        if not seat_row.empty and scol and scol in seat_row.columns:
            try:
                seats_available = int(seat_row.iloc[0][scol])
            except:
                seats_available = 0
            
            if seats_available > 0:
                # Allocate seat
                seats.loc[seat_row.index, scol] = seats_available - 1
                seats.loc[seat_row.index, "TOTAL No. of students admitted"] = int(seat_row.iloc[0]["TOTAL No. of students admitted"]) + 1
                allocated_college = collegeid
                allocated_pref = prefnumber
                break  # stop after successful allocation
    
    # Record result (required columns + new fields)
    output.append({
        'UniqueID': uid,
        'Name': srow.get('Name', ''),  # New field
        'Gender': gender,
        'Caste': caste,
        'Rank': srow.get('Rank', ''),  # New field
        'CollegeID': allocated_college,
        'Institution': seats.loc[seat_row.index, 'Institution'].values[0] if allocated_college else '',  # New field
        'PrefNumber': allocated_pref
    })

# Save to CSV (IDs kept as text, PrefNumber as integer)
out_df = pd.DataFrame(output)
out_df['UniqueID'] = out_df['UniqueID'].astype(str)
out_df['CollegeID'] = out_df['CollegeID'].astype(str)
out_df['PrefNumber'] = out_df['PrefNumber'].astype('Int64')  # keeps int format, blanks allowed

out_df.to_csv("student_allocations.csv", index=False,
              columns=['UniqueID','Name','Gender','Caste','Rank','CollegeID','Institution','PrefNumber'])

