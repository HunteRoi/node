#!/bin/bash

function ask_local_path() {
    read -p "Please provide the local directory path (absolute) as an argument: " local_directory
}

function remove_data() {
    read -p "Do you want to remove the data directory? [Yes/No] " remove_data_choice
    
    if [ "$remove_data_choice" == "Yes" ] || [ "$remove_data_choice" == "yes" ] || [ "$remove_data_choice" == "Y" ] || [ "$remove_data_choice" == "y" ]; then
        ask_local_path        
        rm -rf $local_directory
    else
        echo "Data directory removal aborted."
    fi
}

function uninstall_requirements() {
    read -p "Do you want to uninstall the requirements? [Yes/No] " uninstall_requirements_choice
    
    if [ "$uninstall_requirements_choice" == "Yes" ] || [ "$uninstall_requirements_choice" == "yes" ] || [ "$uninstall_requirements_choice" == "Y" ] || [ "$uninstall_requirements_choice" == "y" ]; then
        su -c "apt-get purge -y curl uidmap iptables && apt-get autoremove -y"
    else
        echo "Requirements uninstallation aborted."
    fi
}

function are_you_sure() {
    read -p "You are trying to fully uninstall a SIDIPP node. Are you sure? [Yes/No] " choice
    
    if [ "$choice" == "Yes" ] || [ "$choice" == "yes" ] || [ "$choice" == "Y" ] || [ "$choice" == "y" ]; then
        echo "Uninstalling..."
        systemctl stop --user docker
        
        su -c "rm -rf /home/$USER/.local/share/docker"
        rm -rf /home/$USER/bin/containerd*
        rm -rf /home/$USER/bin/docker*
        rm -rf /home/$USER/bin/rootlesskit*
        rm -rf /home/$USER/bin/vpnkit
        rm -rf /home/$USER/bin/ctr
        rm -rf /home/$USER/bin/runc
        rm -rf /home/$USER/.docker
        rm -rf /home/$USER/.config/systemd/user/docker.service
        rm -rf /home/$USER/.config/systemd/user/default.target.wants/docker.service
        remove_data
        
        systemctl --user daemon-reload
        echo "Uninstallation complete."
    else
        echo "Uninstallation aborted."
        exit 1
    fi
}

are_you_sure
