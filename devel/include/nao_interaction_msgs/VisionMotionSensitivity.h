// Generated by gencpp from file nao_interaction_msgs/VisionMotionSensitivity.msg
// DO NOT EDIT!


#ifndef NAO_INTERACTION_MSGS_MESSAGE_VISIONMOTIONSENSITIVITY_H
#define NAO_INTERACTION_MSGS_MESSAGE_VISIONMOTIONSENSITIVITY_H

#include <ros/service_traits.h>


#include <nao_interaction_msgs/VisionMotionSensitivityRequest.h>
#include <nao_interaction_msgs/VisionMotionSensitivityResponse.h>


namespace nao_interaction_msgs
{

struct VisionMotionSensitivity
{

typedef VisionMotionSensitivityRequest Request;
typedef VisionMotionSensitivityResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct VisionMotionSensitivity
} // namespace nao_interaction_msgs


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::nao_interaction_msgs::VisionMotionSensitivity > {
  static const char* value()
  {
    return "ef4dcf0f6275a2f726c89cb40c7fcf0f";
  }

  static const char* value(const ::nao_interaction_msgs::VisionMotionSensitivity&) { return value(); }
};

template<>
struct DataType< ::nao_interaction_msgs::VisionMotionSensitivity > {
  static const char* value()
  {
    return "nao_interaction_msgs/VisionMotionSensitivity";
  }

  static const char* value(const ::nao_interaction_msgs::VisionMotionSensitivity&) { return value(); }
};


// service_traits::MD5Sum< ::nao_interaction_msgs::VisionMotionSensitivityRequest> should match 
// service_traits::MD5Sum< ::nao_interaction_msgs::VisionMotionSensitivity > 
template<>
struct MD5Sum< ::nao_interaction_msgs::VisionMotionSensitivityRequest>
{
  static const char* value()
  {
    return MD5Sum< ::nao_interaction_msgs::VisionMotionSensitivity >::value();
  }
  static const char* value(const ::nao_interaction_msgs::VisionMotionSensitivityRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::nao_interaction_msgs::VisionMotionSensitivityRequest> should match 
// service_traits::DataType< ::nao_interaction_msgs::VisionMotionSensitivity > 
template<>
struct DataType< ::nao_interaction_msgs::VisionMotionSensitivityRequest>
{
  static const char* value()
  {
    return DataType< ::nao_interaction_msgs::VisionMotionSensitivity >::value();
  }
  static const char* value(const ::nao_interaction_msgs::VisionMotionSensitivityRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::nao_interaction_msgs::VisionMotionSensitivityResponse> should match 
// service_traits::MD5Sum< ::nao_interaction_msgs::VisionMotionSensitivity > 
template<>
struct MD5Sum< ::nao_interaction_msgs::VisionMotionSensitivityResponse>
{
  static const char* value()
  {
    return MD5Sum< ::nao_interaction_msgs::VisionMotionSensitivity >::value();
  }
  static const char* value(const ::nao_interaction_msgs::VisionMotionSensitivityResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::nao_interaction_msgs::VisionMotionSensitivityResponse> should match 
// service_traits::DataType< ::nao_interaction_msgs::VisionMotionSensitivity > 
template<>
struct DataType< ::nao_interaction_msgs::VisionMotionSensitivityResponse>
{
  static const char* value()
  {
    return DataType< ::nao_interaction_msgs::VisionMotionSensitivity >::value();
  }
  static const char* value(const ::nao_interaction_msgs::VisionMotionSensitivityResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // NAO_INTERACTION_MSGS_MESSAGE_VISIONMOTIONSENSITIVITY_H
