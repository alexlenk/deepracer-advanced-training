#include <gazebo/gazebo.hh>
#include <stdio.h>
#include <stdlib.h>

namespace gazebo
{
  class SystemBashWriter : public SystemPlugin
  {
    /////////////////////////////////////////////
    /// \brief Destructor
    public: virtual ~SystemBashWriter()
    {

    }

    /////////////////////////////////////////////
    /// \brief Called after the plugin has been constructed.
    public: void Load(int /*_argc*/, char ** /*_argv*/)
    {

    }

    /////////////////////////////////////////////
    // \brief Called once after Load
    private: void Init()
    {
        //ROS_INFO("ROS: SystemBashWriter loaded...!");
        gzmsg << "GZ: SystemBashWriter loaded..." << std::endl;
        system("echo Bash: ######### SYSTEM SystemBashWriter Loaded ########");
	system("touch /tmp/works");
        system("cp -rf /home/robomaker/workspace/applications/simulation-application/bundle/opt/install/deepracer_simulation_environment/share/deepracer_simulation_environment/meshes.org /home/robomaker/meshes");
    }

    /////////////////////////////////////////////
    /// \brief Called every PreRender event. See the Load function.
    private: void Update()
    {

    }

  };

  // Register this plugin with the simulator
  GZ_REGISTER_SYSTEM_PLUGIN(SystemBashWriter)
}

