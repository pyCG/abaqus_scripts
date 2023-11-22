if execute_export_abaqus_output == True:
    import subprocess

    # Change directory
    subprocess.run(['cd', directory_path], shell=True, check=True)

    # Execute Abaqus command
    abaqus_script = r'cg_export_stress_displacement_v3.py'
    subprocess.run(['abaqus', 'cae', 'noGUI=' + abaqus_script], shell=True, check=True)
