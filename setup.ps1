$commands = "npm", "conda"
foreach ($command in $commands)
{
    if ((Get-Command $command -ErrorAction SilentlyContinue) -eq $null)
    {
        Write-Host "Unable to find " $command " in path"
        exit
    }
}


Write-Host "existing environments will be listed below:"
Invoke-Expression "conda env list"
$env = Read-Host -Prompt "If you have already defined a favorite conda environment (env), 
you can enter the environment's name now, otherwise enter a new one"
if (!$env)
{
    $env = 'Semi-ATE'
}

$root_location = $(Get-Location)
$webui_location = "ATE/Tester/TES/ui/angular/mini-sct-gui"
$plugin_location = "Plugins/TDKMicronas"
$spyder_location = ".."
$smoke_test_location = "tests/ATE/spyder/widgets/CI/qt/smoketest"
$apps_location = "ATE/Tester/TES/apps"
$package_is_uptodate = $False
$confirm = "y"

function Install-Dependencies {
    Write-Host "install requirements"
    Invoke-Expression "pip install spyder"
    Invoke-Expression "conda install --file requirements/run.txt -y"

    Write-Host "install test requirements"
    Invoke-Expression "conda install --file requirements/test.txt -y"

    Write-Host "install ATE package"
    Invoke-Expression "python setup.py develop"

    Write-Host "install TDKMicronas plugin package"
    Invoke-Expression "cd $plugin_location"
    Invoke-Expression "python setup.py develop"

    # Invoke-Expression "conda install jedi==0.17.2 -y"
    # Invoke-Expression "conda install spyder==3.3.6 -y"
}


try
{
    Invoke-Expression "conda deactivate"
    Invoke-Expression "conda activate $env"
    Write-Host "conda environment: " $env " is activated"
}
catch
{
    Write-Host "new conda environment: " $env " will be generated"
    $confirmation = Read-Host "are you sure you want proceed and create the new environment [y/n]"
    $package_is_uptodate = $True
    
    if (($confirmation -eq $confirm) -or (!$confirmation))
    {
        Write-Host "create new conda environment: " $env
        Invoke-Expression "conda create -n $env python=3.7 -y"
        Invoke-Expression "conda config --append channels conda-forge"
        Invoke-Expression "conda deactivate $env"
        Invoke-Expression "conda activate $env"

        Install-Dependencies
    }

    Set-Location -Path $root_location
}

$confirmation = Read-Host "do you want to build web-UI disctribution [y/n]"
if (($confirmation -eq $confirm) -or (!$confirmation))
{
    Write-Host "install angular cli dependencies"
    Invoke-Expression "npm i -g @angular/cli"

    Write-Host "install web-UI dependencies"
    Invoke-Expression "cd $webui_location"
    Invoke-Expression "npm install"
    Invoke-Expression "npm audit fix"

    Write-Host "generate web-UI distribution"
    Invoke-Expression "ng build"
    Set-Location -Path $root_location
}


if ($null -eq (Get-Command "git" -ErrorAction SilentlyContinue))
{
    Write-Host "Unable to find git in path, spyder sources cannot be imported"
} else
{
    $confirmation = Read-Host "do you want to get spyder sources [y/n]"
    if (($confirmation -eq $confirm) -or (!$confirmation))
    {
        Set-Location -Path $spyder_location
        $spyder = $(Get-Location)
        Invoke-Expression "git clone https://github.com/spyder-ide/spyder.git"
        Invoke-Expression "git checkout 9b2aa14"
        Write-Host "to run spyder-IDE use the following command, first change directroy to: " $spyder
        Write-Host "python bootstrap.py"
    }
}

Set-Location -Path $root_location
if ($package_is_uptodate -ne $True)
{
    $confirmation = Read-Host "do you want to install packages again [y/n]"
    if (($confirmation -eq $confirm) -or (!$confirmation))
    {
        Install-Dependencies
    }
}


Set-Location -Path $root_location
Write-Host "build test program"
Invoke-Expression "pytest $smoke_test_location"
Invoke-Expression "Copy-Item  -Path $smoke_test_location -Destination ./ -Recurse -force"

Write-Host "new configuration file for master and control Apps will be generated"
$confirmation = Read-Host "are you sure you want proceed and create new configuration files [y/n]"
if (($confirmation -eq $confirm) -or (!$confirmation))
{
    Set-Location -Path $apps_location

    Write-Host "generate control_app configuration file"
    Invoke-Expression "python auto_script.py control SCT-81-1F -conf"
    Write-Host "done"

    Write-Host "generate master_app configuration file"
    Invoke-Expression "python auto_script.py master SCT-81-1F -conf"
    Write-Host "done"

    Invoke-Expression "cp le123456000_template.xml le123456000.xml"

    Write-Host "testprogram name must be adapted in ATE/Tester/TES/apps/le123456000.xml, therefore replace the 'PROGRAM_DIR#' field inside
                'STATION' section with the following:"
    $testprogram_location = "smoketest/smoke_test/src/HW0/PR/smoke_test_HW0_PR_Die1_Production_PR_1.py"
    Write-Host "(make sure you copy the absolut path!!) => test program path: " $testprogram_location

    Write-Host "now you should be able to start control, master and test-application"
}

Write-Host ""
Write-Host ""
Write-Host "                        !!!!!!!!!!!!!!!!!!!!!!! ATTENTION !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
Write-Host "                        please make sure you read the instruction from README.md file"
