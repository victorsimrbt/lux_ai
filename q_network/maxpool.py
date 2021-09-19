from keras.models import Model,Input
from keras.layers import Conv2D,BatchNormalization,add,Activation,Dense,MaxPooling3D,Reshape
from keras.losses import CategoricalCrossentropy,MeanSquaredError

def residual_module(layer_in, n_filters):
    merge_input = layer_in
    if layer_in.shape[-1] != n_filters:
        merge_input = Conv2D(
            n_filters, (1, 1), padding='same', activation='relu')(layer_in)
    conv1 = Conv2D(n_filters, (3, 3), padding='same',
                    activation='relu')(layer_in)
    batch_norm = BatchNormalization()(conv1)
    layer_out = add([batch_norm, merge_input])
    layer_out = Activation('relu')(layer_out)
    return layer_out

visible = Input(shape=(23,32,32))
reshaped_input = Reshape((23,32,32,1))(visible)
layer1 = residual_module(reshaped_input, 64)
layer2 = residual_module(layer1, 128)
layer3 = residual_module(layer1, 256)
layer3 = residual_module(layer2, 32)
pool = MaxPooling3D(pool_size = (23,1,1))(layer3)
dense1 = Dense(64,activation = 'relu')(pool)
dense2 = Dense(128,activation = 'relu')(dense1)
dense3 = Dense(256,activation = 'relu')(dense2)
dense4 = Dense(1037,activation = 'relu')(dense3)
output = Reshape((32,32,1037))(dense4)

model = Model(inputs=visible, outputs=output)
model.summary()