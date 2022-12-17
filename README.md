# Post-processing algorithms for PHY-Based Key Agreement Scheme Using Aerial Audio Networking

##  General description
This project is based on the research work done as part of PhD Thesis. This part is titled under “PHY-Based Key Agreement Scheme Using Aerial Audio Networking”, where we propose a physical layer security based solution that exploits the physical characteristics of the wireless channel in general, and the attractive features of the audio channel as an appealing technique to be used as a user-friendly, room-contained key agreement scheme, to generate a secret key between two smartphones that are located in the same room. 

For more details and better understanding of the project and its goals, the reader is referred to the original paper:

[1] PHY Based Key Agreement Scheme using Audio Networking

@inproceedings{bala2020phy,
  title={Phy-based key agreement scheme using audio networking},
  author={Bala, Dania Qara and Raman, Bhaskaran},
  booktitle={2020 International Conference on COMmunication Systems \& NETworkS (COMSNETS)},
  pages={129--136},
  year={2020},
  organization={IEEE}
}

Our Proposed Audio Networking PHY-Based Key Agreement contains the following steps:
1.	Audio Channel Probing and Measurements Extraction: The output of this step is the audio files in .wav format  recorded by the entities included in the experiments.
2.	Chunk-Wise Quantisation
3.	Cascade Based Information Reconciliation
4.	Privacy Amplification

The first step (Audio Channel Probing and Measurements Extraction) is implemented in an Android Application that can
 be found in our repository (https://github.com/BaQaDa/First-Step-PHY-Based-Key-Agreement-Scheme-Using-Aerial-Audio-Networking/blob/master/README.md). 

While the remaining steps are implemented in Python, as shown in the current repository. The
 repository contains our implementation of the next steps (Chunk-Wise Quantisation, Cascade Based Information Reconciliation, Privacy Amplification) used for the post-processing procedure of the PHY Based Key Agreement Scheme using Audio Networking. Additionally, the repository contains an analysis of some main properties of audio networking that influence the design of the proposed key agreement system such as ambient noise, and locality property.

The entities considered for the experiments are: Two smartphones are set as the legitimate end-parties A and B. For the purpose of security analysis, a third phone is set as an adversary, namely, eavesdropper E. E can either eavesdrop on A or B. In the underlying experiment, E is configured to eavesdrop on A. For more details, please refer to the original paper 

[1] PHY Based Key Agreement Scheme using Audio Networking

##	Folders' contents
Here we briefly describe the main `.py` scripts presented in the repository. 
 
### `Generate_Key`

The folder contains `.py` scripts related to the authentication procedure.
1.	 `select_parameters_KGR_BCR_one_window-plot.py`:
The input to this file is the audio files recorded by the entities included in the experiment
The file plots the different values of Key Generation Rate (KGR) and Bit Conflict Rate (BCR) that our system can achieve for varying chunk-size at various values of alpha parameters. Based on the graphs we select the proper parameter values to obtain high KGR while maintaining the BCR as small as possible. The selected values are then manually entered in the `run_file_get_keys.py` file.
2.	`run_file_get_keys.py`:
Uses the `.py` scripts in (quantize_reconcile_amplify_privacy) folder.
The input to this file is the audio files recorded by the entities included in the experiment, and the parameters’ selected values.  The `run_file_get_keys.py` performs the three post-processing steps for each of the pairs (A and B) and (A and E). The results are K_AB between the legitimate end-parties (A and B) and the key K_AE that the eavesdropper E would infer on running the same key agreement process. The shared key K_AB obtained at the legitimate end-parties, A and B, is different from the key K_AE inferred by E.


### `quantize_reconcile_amplify_privacy`
This folder contains `.py` scripts related to the post-processing steps: 1. Chunk-Wise Quantisation, 2. Cascade Based Information Reconciliation, 3. Privacy Amplification. 

### `_0_signal_processing_functions`
### `_1_signal_processing_applied_files`
These folders contain some `.py`  files with auxiliary functions used by the different algorithms. Some of these functions are related to signal processing, plotting signals, and checking for features as ambient noise, locality property. 

## Notes 
To examine the randomness of our generated key, we apply NIST SP 800-22 statistical test suit. A python implementation of the SP800-22 Rev 1a PRNG test suite can be found in the repository (https://github.com/dj-on-github/sp800_22_tests). 
