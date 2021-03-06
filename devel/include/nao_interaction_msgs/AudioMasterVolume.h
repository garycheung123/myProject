// Generated by gencpp from file nao_interaction_msgs/AudioMasterVolume.msg
// DO NOT EDIT!


#ifndef NAO_INTERACTION_MSGS_MESSAGE_AUDIOMASTERVOLUME_H
#define NAO_INTERACTION_MSGS_MESSAGE_AUDIOMASTERVOLUME_H

#include <ros/service_traits.h>


#include <nao_interaction_msgs/AudioMasterVolumeRequest.h>
#include <nao_interaction_msgs/AudioMasterVolumeResponse.h>


namespace nao_interaction_msgs
{

struct AudioMasterVolume
{

typedef AudioMasterVolumeRequest Request;
typedef AudioMasterVolumeResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct AudioMasterVolume
} // namespace nao_interaction_msgs


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::nao_interaction_msgs::AudioMasterVolume > {
  static const char* value()
  {
    return "6a2d45c5fcf9fd89299667da81b32d64";
  }

  static const char* value(const ::nao_interaction_msgs::AudioMasterVolume&) { return value(); }
};

template<>
struct DataType< ::nao_interaction_msgs::AudioMasterVolume > {
  static const char* value()
  {
    return "nao_interaction_msgs/AudioMasterVolume";
  }

  static const char* value(const ::nao_interaction_msgs::AudioMasterVolume&) { return value(); }
};


// service_traits::MD5Sum< ::nao_interaction_msgs::AudioMasterVolumeRequest> should match 
// service_traits::MD5Sum< ::nao_interaction_msgs::AudioMasterVolume > 
template<>
struct MD5Sum< ::nao_interaction_msgs::AudioMasterVolumeRequest>
{
  static const char* value()
  {
    return MD5Sum< ::nao_interaction_msgs::AudioMasterVolume >::value();
  }
  static const char* value(const ::nao_interaction_msgs::AudioMasterVolumeRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::nao_interaction_msgs::AudioMasterVolumeRequest> should match 
// service_traits::DataType< ::nao_interaction_msgs::AudioMasterVolume > 
template<>
struct DataType< ::nao_interaction_msgs::AudioMasterVolumeRequest>
{
  static const char* value()
  {
    return DataType< ::nao_interaction_msgs::AudioMasterVolume >::value();
  }
  static const char* value(const ::nao_interaction_msgs::AudioMasterVolumeRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::nao_interaction_msgs::AudioMasterVolumeResponse> should match 
// service_traits::MD5Sum< ::nao_interaction_msgs::AudioMasterVolume > 
template<>
struct MD5Sum< ::nao_interaction_msgs::AudioMasterVolumeResponse>
{
  static const char* value()
  {
    return MD5Sum< ::nao_interaction_msgs::AudioMasterVolume >::value();
  }
  static const char* value(const ::nao_interaction_msgs::AudioMasterVolumeResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::nao_interaction_msgs::AudioMasterVolumeResponse> should match 
// service_traits::DataType< ::nao_interaction_msgs::AudioMasterVolume > 
template<>
struct DataType< ::nao_interaction_msgs::AudioMasterVolumeResponse>
{
  static const char* value()
  {
    return DataType< ::nao_interaction_msgs::AudioMasterVolume >::value();
  }
  static const char* value(const ::nao_interaction_msgs::AudioMasterVolumeResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // NAO_INTERACTION_MSGS_MESSAGE_AUDIOMASTERVOLUME_H
